import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker, useMap } from 'react-leaflet';
import L from 'leaflet';
import './MapView.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const getRiskColor = (riskLevel) => {
  switch (riskLevel) {
    case 'CRITICAL':
      return '#e53e3e';
    case 'HIGH':
      return '#ed8936';
    case 'MEDIUM':
      return '#ecc94b';
    case 'LOW':
      return '#48bb78';
    default:
      return '#cbd5e0';
  }
};

// Component to fit map bounds to show all markers
function FitBounds({ assets }) {
  const map = useMap();
  
  useEffect(() => {
    if (assets && assets.length > 0) {
      try {
        const bounds = L.latLngBounds(
          assets.map(asset => [asset.lat, asset.lon])
        );
        // Use setTimeout to ensure map is fully rendered
        setTimeout(() => {
          map.fitBounds(bounds, { padding: [80, 80], maxZoom: 13 });
        }, 100);
      } catch (error) {
        console.error('Error fitting bounds:', error);
      }
    }
  }, [assets, map]);
  
  return null;
}

const MapView = ({ assets, risks }) => {
  const londonCenter = [51.5074, -0.1278];

  // Create a map of asset_id -> risk
  const riskMap = {};
  if (risks && Array.isArray(risks)) {
    risks.forEach((risk) => {
      riskMap[risk.asset_id] = risk;
    });
  }

  // Debug logging
  useEffect(() => {
    console.log('MapView - Assets:', assets);
    console.log('MapView - Risks:', risks);
    console.log('MapView - Asset count:', assets?.length || 0);
  }, [assets, risks]);

  return (
    <div className="map-view">
      <MapContainer
        center={londonCenter}
        zoom={11}
        style={{ height: '100%', width: '100%', minHeight: '100%' }}
        dragging={false}
        touchZoom={false}
        doubleClickZoom={false}
        scrollWheelZoom={false}
        zoomControl={false}
        boxZoom={false}
        keyboard={false}
        whenReady={(map) => {
          // Ensure map is properly sized
          setTimeout(() => {
            map.target.invalidateSize();
          }, 100);
        }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <FitBounds assets={assets} />
        
        {assets && Array.isArray(assets) && assets.length > 0 ? (
          assets.map((asset) => {
            if (!asset.lat || !asset.lon) {
              console.warn('Asset missing coordinates:', asset);
              return null;
            }
            
            const risk = riskMap[asset.id];
            const color = risk ? getRiskColor(risk.risk_level) : '#cbd5e0';
            
            return (
              <CircleMarker
                key={asset.id || `asset-${asset.lat}-${asset.lon}`}
                center={[parseFloat(asset.lat), parseFloat(asset.lon)]}
                radius={14}
                pathOptions={{ 
                  color: '#ffffff', 
                  fillColor: color, 
                  fillOpacity: 1, 
                  weight: 4,
                  opacity: 1
                }}
                eventHandlers={{
                  click: (e) => {
                    e.target.openPopup();
                  },
                  mouseover: (e) => {
                    e.target.setStyle({
                      weight: 6,
                      fillOpacity: 1,
                      radius: 16
                    });
                  },
                  mouseout: (e) => {
                    e.target.setStyle({
                      weight: 4,
                      fillOpacity: 1,
                      radius: 14
                    });
                  }
                }}
              >
                <Popup>
                  <div className="asset-popup">
                    <h4>{asset.name}</h4>
                    <p><strong>Type:</strong> {asset.type}</p>
                    <p><strong>ID:</strong> {asset.id}</p>
                    <p><strong>Capacity:</strong> {asset.capacity_kw} kW</p>
                    <p><strong>Criticality:</strong> {asset.criticality}</p>
                    {risk && (
                      <div className="risk-info">
                        <p><strong>Risk:</strong> <span style={{ color }}>{risk.risk_level}</span></p>
                        <p><strong>Reason:</strong> {risk.reason}</p>
                        <p><strong>Impact:</strong> {risk.expected_impact}</p>
                      </div>
                    )}
                  </div>
                </Popup>
              </CircleMarker>
            );
          })
        ) : (
          // Show a test marker at center when no assets
          <CircleMarker
            center={londonCenter}
            radius={14}
            pathOptions={{ 
              color: '#ffffff', 
              fillColor: '#3b82f6', 
              fillOpacity: 1, 
              weight: 4,
              opacity: 1
            }}
          >
            <Popup>
              <div className="asset-popup">
                <p><strong>London Center</strong></p>
                <p>Run a scenario to see asset markers on the map.</p>
              </div>
            </Popup>
          </CircleMarker>
        )}
      </MapContainer>
      
      <div className="map-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#e53e3e' }}></span>
          <span>Critical</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ed8936' }}></span>
          <span>High</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ecc94b' }}></span>
          <span>Medium</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#48bb78' }}></span>
          <span>Low</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#cbd5e0' }}></span>
          <span>No Risk</span>
        </div>
      </div>
    </div>
  );
};

export default MapView;

