import { createRoot } from "react-dom/client";
import { BrowserRouter, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./styles.css";
import LoginPage from "./pages/LoginPage";
import ScenarioListPage from "./pages/ScenarioListPage";
import SimulationPage from "./pages/SimulationPage";
import ReportPage from "./pages/ReportPage";
import ReplayPage from "./pages/ReplayPage";
import FeedbackPage from "./pages/FeedbackPage";
import PilotDashboardPage from "./pages/PilotDashboardPage";
import FirstRunWizard from "./components/FirstRunWizard";
import ErrorBoundary from "./components/ErrorBoundary";
import ErrorPanel from "./components/ErrorPanel";
import type { ScenarioSummary } from "./lib/types";
import { friendlyError, type UserFacingError } from "./lib/errors";
import * as api from "./lib/api";
import { trackApplicationOpened } from "./lib/analytics";
import { useEffect } from "react";

function App() {
  const navigate = useNavigate();
  const [token, setToken] = useState<string | null>(
    () => sessionStorage.getItem("callibr_token"),
  );
  const [user, setUser] = useState<{ display_name: string } | null>(null);
  const [scenarios, setScenarios] = useState<ScenarioSummary[]>([]);
  const [scenariosLoaded, setScenariosLoaded] = useState(false);
  const [scenariosError, setScenariosError] =
    useState<UserFacingError | null>(null);
  const [loadAttempt, setLoadAttempt] = useState(0);

  useEffect(() => {
    trackApplicationOpened();
  }, []);

  useEffect(() => {
    if (!token) return;
    setScenariosError(null);
    api
      .listScenarios(token)
      .then((list) => {
        setScenarios(list);
        setScenariosLoaded(true);
      })
      .catch((err) => setScenariosError(friendlyError(err)));
  }, [token, loadAttempt]);

  if (!token) {
    return <LoginPage onLogin={(t, u) => {
      sessionStorage.setItem("callibr_token", t);
      setToken(t);
      setUser(u);
    }} />;
  }

  if (scenariosError) {
    return (
      <div className="login-page">
        <div className="login-card">
          <ErrorPanel
            error={scenariosError}
            onRetry={() => setLoadAttempt((n) => n + 1)}
          />
        </div>
      </div>
    );
  }

  if (!scenariosLoaded) {
    return (
      <LoginPage
        onLogin={(t, u) => {
          sessionStorage.setItem("callibr_token", t);
          setToken(t);
          setUser(u);
        }}
      />
    );
  }

  const firstRunDone = localStorage.getItem("callibr_first_run") === "done";
  if (!firstRunDone) {
    return (
      <FirstRunWizard
        token={token}
        scenarios={scenarios}
      />
    );
  }

  return (
    <div className="app-shell">
      <header className="app-topbar">
        <div className="topbar-left">
          <span className="topbar-brand">Callibr</span>
          <span className="topbar-user">{user?.display_name ?? "Apprenant"}</span>
        </div>
        <nav className="topbar-nav">
          <button className="topbar-link" onClick={() => navigate("/dashboard")} type="button">
            Tableau de bord
          </button>
          <button className="topbar-link" onClick={() => navigate("/scenarios")} type="button">
            Scénarios
          </button>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route
            element={<ScenarioListPage scenarios={scenarios} token={token} />}
            path="/scenarios"
          />
          <Route
            element={<SimulationPage token={token} />}
            path="/simulation"
          />
          <Route
            element={<ReportPage token={token} />}
            path="/report"
          />
          <Route
            element={<PilotDashboardPage token={token} />}
            path="/dashboard"
          />
          <Route
            element={<ReplayPage token={token} />}
            path="/replay"
          />
          <Route
            element={
              <FeedbackPage
                sessionId={new URLSearchParams(window.location.search).get("session") ?? ""}
                token={token}
              />
            }
            path="/feedback"
          />
          <Route
            element={<Navigate replace to="/scenarios" />}
            path="*"
          />
        </Routes>
      </main>
    </div>
  );
}

const root = createRoot(document.getElementById("root") as HTMLElement);
root.render(
  <BrowserRouter>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </BrowserRouter>,
);
