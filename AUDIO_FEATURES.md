# 🎵 Audio Atmosphere Features

## Overview

CoconuT-Ai now includes an immersive audio atmosphere system that enhances your chat experience with mood-based ambient sounds and music playback capabilities.

## Features

### 🌊 Mood-Based Ambient Sounds

The chatbot automatically plays ambient sounds that match your detected mood:

- **Happy** 😊 - Upbeat, positive ambient music
- **Sad** 😢 - Calming rain and peaceful sounds
- **Angry** 😠 - Tension relief ambient music
- **Neutral** 😐 - Peaceful ambient sounds
- **Surprise** 😮 - Wonder and curiosity sounds
- **Fear** 😨 - Calming, reassuring sounds
- **Disgust** 🤢 - Neutral ambient background

### 🎵 Music Player

Built-in music player with current track display showing:
- Album artwork
- Song title
- Artist names
- Album information

### 🎛️ Audio Controls

Located in the side panel:

1. **Ambient Sounds Toggle** - Turn ambient sounds on/off
2. **Ambient Volume Slider** - Adjust ambient sound volume (0-100%)
3. **Music Player Toggle** - Play/pause music
4. **Music Volume Slider** - Adjust music volume (0-100%)
5. **Now Playing Display** - Shows current song information

## How It Works

1. **Automatic Start**: When you complete mood detection, ambient sounds matching your mood automatically start playing
2. **Mood Changes**: Ambient sounds smoothly transition when your mood changes
3. **Volume Mixing**: Both ambient sounds and music can play simultaneously with independent volume controls
4. **Smart Fading**: Smooth fade-out/fade-in transitions when changing sounds

## Adding New Songs

### Sample Song Data

Here's how the BIBA song is configured:

```javascript
{
    'biba': {
        title: 'BIBA',
        artists: 'Marshmello, Pritam Chakraborty, Shirley Setia, Pardeep Singh Sran, Dev Negi',
        album: 'BIBA',
        url: 'http://h.saavncdn.com/987/cd902d048c13e5ce6ca84cc409746a5d.mp3',
        image: 'https://c.saavncdn.com/987/BIBA-English-2019-20190201201359-500x500.jpg',
        duration: 175,
        year: 2019
    }
}
```

### Adding More Songs

To add more songs to the library:

1. Open `static/js/main.js`
2. Find the `songLibrary` object (around line 20)
3. Add your song following this format:

```javascript
const songLibrary = {
    'biba': {
        title: 'BIBA',
        artists: 'Marshmello, Pritam Chakraborty, Shirley Setia, Pardeep Singh Sran, Dev Negi',
        album: 'BIBA',
        url: 'http://h.saavncdn.com/987/cd902d048c13e5ce6ca84cc409746a5d.mp3',
        image: 'https://c.saavncdn.com/987/BIBA-English-2019-20190201201359-500x500.jpg',
        duration: 175,
        year: 2019
    },
    // Add your new song here
    'your_song_id': {
        title: 'Song Title',
        artists: 'Artist Names',
        album: 'Album Name',
        url: 'https://your-song-url.mp3',
        image: 'https://album-cover-url.jpg',
        duration: 180, // in seconds
        year: 2024
    }
};
```

### Playing Different Songs

To play a specific song, modify the music toggle function:

```javascript
// In main.js, find toggleMusic() function
function toggleMusic() {
    if (isMusicPlaying) {
        stopMusic();
    } else {
        // Change 'biba' to your song ID
        playMusic('your_song_id');
    }
}
```

## Customizing Ambient Sounds

### Changing Mood Sounds

To use different ambient sounds for specific moods:

1. Open `static/js/main.js`
2. Find the `ambientSounds` object (around line 14)
3. Replace the URL with your preferred ambient sound:

```javascript
const ambientSounds = {
    'happy': 'YOUR_UPBEAT_AMBIENT_URL.mp3',
    'sad': 'YOUR_CALMING_AMBIENT_URL.mp3',
    // ... etc
};
```

### Free Ambient Sound Resources

- [Pixabay Audio](https://pixabay.com/music/) - Free ambient sounds
- [Freesound](https://freesound.org/) - Community sound library
- [YouTube Audio Library](https://www.youtube.com/audiolibrary) - Royalty-free music
- [Incompetech](https://incompetech.com/) - Creative Commons music

## Usage Tips

1. **Enable Audio First**: Click the ambient sound toggle to enable browser audio playback
2. **Volume Levels**: Recommended settings:
   - Ambient: 20-40% for background atmosphere
   - Music: 40-60% for primary listening
3. **Mixed Playback**: Lower ambient volume when playing music for better balance
4. **Mood-Based Experience**: Let ambient sounds change with your mood for an adaptive experience

## Technical Details

### Audio System Architecture

- **Dual Audio Players**: Separate `<audio>` elements for ambient and music
- **Loop Control**: Ambient sounds loop continuously, music plays once
- **Volume Management**: Independent volume controls with smooth transitions
- **Browser Compatibility**: Uses standard HTML5 Audio API

### Key Functions

- `initializeAudioSystem()` - Initializes audio players
- `playAmbientSound(mood)` - Plays ambient sound for specific mood
- `playMusic(songId)` - Plays music from song library
- `changeAmbientSound(mood)` - Smoothly transitions to new ambient sound
- `updateNowPlaying(song)` - Updates Now Playing display

### Auto-Play Handling

Modern browsers require user interaction before playing audio. The system:
1. Waits for mood detection completion (user interaction)
2. Automatically starts ambient sounds
3. Shows notification if audio playback is blocked

## Troubleshooting

### Audio Not Playing

1. Check browser console for errors
2. Ensure URLs are accessible (check CORS)
3. Click the toggle buttons to enable audio
4. Check volume sliders are not at 0

### Sound Quality Issues

1. Use high-quality audio files (128kbps or higher)
2. Ensure stable internet connection
3. Check audio file formats (MP3 recommended)

### Volume Too Loud/Soft

- Adjust volume sliders in the Audio Atmosphere panel
- Recommended: Ambient 30%, Music 50%

## Future Enhancements

Potential features to add:

- [ ] Playlist support
- [ ] Music search integration (JioSaavn, Spotify API)
- [ ] Custom ambient sound upload
- [ ] Audio visualizer
- [ ] Equalizer controls
- [ ] Crossfade duration settings
- [ ] Song queue management
- [ ] Save audio preferences

## License & Copyright

- Ambient sounds: Free use from Pixabay (Pixabay License)
- Music: Ensure you have proper licensing for any commercial use
- JioSaavn: Songs are streamed from JioSaavn - respect their terms of service

---

**Enjoy your enhanced audio experience with CoconuT-Ai! 🎵🥥🤖**
