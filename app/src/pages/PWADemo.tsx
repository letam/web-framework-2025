import type { ReactElement } from "react";
import { useNavigate } from "react-router";
import { useState } from "react";
import reactLogo from '../assets/react.svg'
import appLogo from '/favicon.svg'
import PWABadge from '../PWABadge.tsx'
import '../PWADemo.css'

function PWADemo(): ReactElement {

    const navigate = useNavigate();
  function goHome(): void {
    navigate("/");
  }

  const [count, setCount] = useState(0)

  return (
    <div id="demo">
    <div id="demo-body">
    <div id="demo-root">
    <button type="button" onClick={goHome}>
        Go home
      </button>
      <div>
        <a href="https://vite.dev" target="_blank" rel="noopener noreferrer">
          <img src={appLogo} className="logo" alt="app logo" />
        </a>
        <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>app</h1>
      <div className="card">
        <button type="button" onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <PWABadge />
    </div>
    </div>
    </div>
  )
}

export default PWADemo;
