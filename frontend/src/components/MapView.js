import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
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

const MapView = ({ assets, risks }) => {
  const londonCenter = [51.5074, -0.1278];

  // Create a map of asset_id -> risk
  const riskMap = {};
  risks.forEach((risk) => {
    riskMap[risk.asset_id] = risk;
  });

  return (
    <div className="map-view">
      <MapContainer
        center={londonCenter}
        zoom={11}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {assets.map((asset) => {
          const risk = riskMap[asset.id];
          const color = risk ? getRiskColor(risk.risk_level) : '#cbd5e0';
          
          return (
            <CircleMarker
              key={asset.id}
              center={[asset.lat, asset.lon]}
              radius={8}
              pathOptions={{ color: 'white', fillColor: color, fillOpacity: 0.8, weight: 2 }}
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
                    </div>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
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

