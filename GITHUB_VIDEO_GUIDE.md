# 🎥 Adding Demo Video to GitHub README

## ✅ Yes! GitHub supports video embeds

You can add YouTube videos to your GitHub README in multiple ways:

---

## Method 1: YouTube Embed (Recommended - Shows Video Player)

Add this to your README.md:

```markdown
## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

**Replace `YOUR_VIDEO_ID`** with your YouTube video ID.

**Example:**
If your YouTube URL is: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
Then your video ID is: `dQw4w9WgXcQ`

**Full example:**
```markdown
## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
```

**Result:** Shows a clickable thumbnail that opens the video on YouTube.

---

## Method 2: Direct YouTube Link (Simple)

```markdown
## 🎬 Demo Video

Watch the demo: [YouTube Demo](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

---

## Method 3: HTML Embed (Full Player - May Not Work on All Browsers)

```html
## 🎬 Demo Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/YOUR_VIDEO_ID" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

**Note:** GitHub may strip HTML, so Method 1 is more reliable.

---

## 📍 Where to Add in README

**Best location:** Right after the title/description, before "Problem Focus"

```markdown
# Grid-Scale Demand Flexibility Agent

An AI-powered agentic orchestration system...

## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

## 🎯 Problem Focus
...
```

---

## 🔍 How to Get Your YouTube Video ID

1. **Upload your video** to YouTube
2. **Copy the URL** from your browser:
   - `https://www.youtube.com/watch?v=ABC123xyz`
   - The part after `v=` is your video ID: `ABC123xyz`

---

## ✨ Enhanced Version (With Description)

```markdown
## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

**Watch the full demo** showing our AI-powered agent forecasting grid risks and orchestrating DERs through Beckn Protocol.

**Demo Highlights:**
- Real-time risk assessment
- AI-powered mitigation planning
- Beckn Protocol execution
```

---

## 🎯 Quick Copy-Paste Template

Once you have your YouTube video URL, use this:

```markdown
## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

**Just replace `YOUR_VIDEO_ID` with your actual video ID!**

---

## ✅ Checklist

- [ ] Video uploaded to YouTube
- [ ] Video is public or unlisted (not private)
- [ ] Got the video ID from URL
- [ ] Added embed code to README.md
- [ ] Tested the link works
- [ ] Committed and pushed to GitHub

---

**That's it! Your demo video will appear in your GitHub README! 🎉**

