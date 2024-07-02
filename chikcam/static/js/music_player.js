document.addEventListener('DOMContentLoaded', function() {
  const audioPlayer = document.getElementById('audio-player');
  const audioSource = document.getElementById('audio-source');
  const stationName = document.getElementById('station-name');
  const trackTitle = document.getElementById('track-title');
  const trackArtist = document.getElementById('track-artist');
  const trackAlbum = document.getElementById('track-album');  // Add this line
  const coverArt = document.getElementById('cover-art');
  const switchStationBtn = document.getElementById('switch-station-btn');

  let currentStationIndex = 0;
  let currentTrackIndex = 0;
  let stations = [];  // Array to store station data fetched from Django

  // Function to load current station and play the first track
  function loadStation(stationIndex) {
      const station = stations[stationIndex];
      stationName.textContent = station.name;
      currentTrackIndex = 0;  // Reset track index when loading a new station
      playTrack(station.tracks[currentTrackIndex]);
  }

  // Function to play a specific track
  function playTrack(track) {
      audioSource.src = track.file_url;  // Assuming 'file_url' is the URL to your audio file
      audioPlayer.load();
      audioPlayer.play();
      trackTitle.textContent = track.title;
      trackArtist.textContent = track.artist;
      trackAlbum.textContent = track.album;  // Add this line
      coverArt.src = track.cover_art_url;  // Assuming 'cover_art_url' is the URL to your cover art image
  }

  // Event listener for switching stations
  switchStationBtn.addEventListener('click', function() {
      currentStationIndex = (currentStationIndex + 1) % stations.length;
      loadStation(currentStationIndex);
  });

  // Event listener for when the current track ends
  audioPlayer.addEventListener('ended', function() {
      const station = stations[currentStationIndex];
      currentTrackIndex = (currentTrackIndex + 1) % station.tracks.length;
      playTrack(station.tracks[currentTrackIndex]);
  });

  // Fetch stations data from Django backend
  fetch('/music_player/api/stations/')
      .then(response => response.json())
      .then(data => {
          stations = data;
          loadStation(currentStationIndex);  // Load initial station
      })
      .catch(error => console.error('Error fetching stations:', error));
});
