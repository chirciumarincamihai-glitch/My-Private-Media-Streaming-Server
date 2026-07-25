import { useState } from 'react';


const API_URL = import.meta.env.VITE_API_URL_SERVER;

function Login({ onLoginSuccess }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('adult');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    const endpoint = isRegistering ? '/register' : '/login';
    const body = isRegistering
      ? { username, password, role }
      : { username, password };

    fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
      .then((response) => response.json().then((data) => ({ status: response.status, data })))
      .then(({ status, data }) => {
        if (status === 200 || status === 201) {
          if (isRegistering) {
            setIsRegistering(false);
            setError('Registered! You can now log in.');
          } else {
            onLoginSuccess(username, role, data.token);
          }
        } else {
          setError(data.error || 'Something went wrong');
        }
      })
      .catch(() => setError('Could not reach the server'));
  };

  return (
    <div className="login-page">
      <div className="login-box">
        <h1>{isRegistering ? 'Create Account' : 'Sign In'}</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {isRegistering && (
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="adult">Adult</option>
              <option value="kid">Kid</option>
            </select>
          )}
          {error && <p className="login-error">{error}</p>}
          <button type="submit">{isRegistering ? 'Register' : 'Sign In'}</button>
        </form>
        <p className="login-toggle" onClick={() => setIsRegistering(!isRegistering)}>
          {isRegistering ? 'Already have an account? Sign in' : "New here? Create an account"}
        </p>
      </div>
    </div>
  );
}

export default Login;