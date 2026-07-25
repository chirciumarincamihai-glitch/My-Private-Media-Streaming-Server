import { useState, useEffect } from 'react';
import Login from './Login';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL_SERVER;

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    if (!currentUser || !token) return;
    fetch(`${API_URL}/list`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setMovies(data))
      .catch((error) => console.error('Error fetching movies:', error));
  }, [currentUser, token]);

  if (!currentUser) {
    return (
      <Login
        onLoginSuccess={(username, role, receivedToken) => {
          setCurrentUser({ username, role });
          setToken(receivedToken);
        }}
      />
    );
  }

  if (selectedMovie) {
    return (
      <div className="player-page">
        <button onClick={() => setSelectedMovie(null)}>← Back to library</button>
        <h2>{selectedMovie.name}</h2>
        <video
          src={`${API_URL}/${selectedMovie.name}?token=${token}`}
          controls
          autoPlay
          className="video-player"
        />
      </div>
    );
  }

  return (
    <div className="library">
      <h1>My Library — Welcome, {currentUser.username}</h1>
      <div className="movie-grid">
        {movies.map((movie) => (
          <div
            key={movie.id}
            className="movie-card"
            onClick={() => setSelectedMovie(movie)}
          >
            <div className="movie-thumbnail">{movie.name.charAt(0)}</div>
            <p>{movie.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;