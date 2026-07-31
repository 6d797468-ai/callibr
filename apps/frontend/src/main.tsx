import { createRoot } from "react-dom/client";
import { BrowserRouter, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import "./styles.css";
import LoginPage from "./pages/LoginPage";
import ScenarioListPage from "./pages/ScenarioListPage";
import SimulationPage from "./pages/SimulationPage";
import ReportPage from "./pages/ReportPage";
import ReplayPage from "./pages/ReplayPage";
import FeedbackPage from "./pages/FeedbackPage";
import PilotDashboardPage from "./pages/PilotDashboardPage";
import SessionsListPage from "./pages/SessionsListPage";
import ReportsListPage from "./pages/ReportsListPage";
import ReplayListPage from "./pages/ReplayListPage";
import FeedbackListPage from "./pages/FeedbackListPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import VoiceHistoryPage from "./pages/VoiceHistoryPage";
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
  const location = useLocation();
  const [token, setToken] = useState<string | null>(
    () => sessionStorage.getItem("callibr_token"),
  );
  const [user, setUser] = useState<{ display_name: string } | null>(null);
  const [scenarios, setScenarios] = useState<ScenarioSummary[]>([]);
  const [scenariosLoaded, setScenariosLoaded] = useState(false);
  const [scenariosError, setScenariosError] =
    useState<UserFacingError | null>(null);
  const [loadAttempt, setLoadAttempt] = useState(0);
  const [activityOpen, setActivityOpen] = useState(false);

  useEffect(() => {
    trackApplicationOpened();
  }, []);

  useEffect(() => {
    setActivityOpen(false);
  }, [location]);

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
          <div className="topbar-dropdown">
            <button
              className="topbar-link"
              onClick={() => setActivityOpen((o) => !o)}
              type="button"
            >
              Mon activité ▾
            </button>
            {activityOpen && (
              <div className="topbar-dropdown-menu">
                <button className="topbar-dropdown-item" onClick={() => { setActivityOpen(false); navigate("/sessions"); }} type="button">
                  Mes simulations
                </button>
                <button className="topbar-dropdown-item" onClick={() => { setActivityOpen(false); navigate("/reports"); }} type="button">
                  Mes rapports
                </button>
                <button className="topbar-dropdown-item" onClick={() => { setActivityOpen(false); navigate("/replay"); }} type="button">
                  Replay
                </button>
                <button className="topbar-dropdown-item" onClick={() => { setActivityOpen(false); navigate("/feedback"); }} type="button">
                  Mes avis
                </button>
              </div>
            )}
          </div>
          <button className="topbar-link" onClick={() => navigate("/analytics")} type="button">
            Analytics
          </button>
          <button className="topbar-link" onClick={() => navigate("/voice")} type="button">
            Voix
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
            path="/replay/session"
          />
          <Route
            element={<SessionsListPage token={token} />}
            path="/sessions"
          />
          <Route
            element={<ReportsListPage token={token} />}
            path="/reports"
          />
          <Route
            element={<ReplayListPage token={token} />}
            path="/replay"
          />
          <Route
            element={<FeedbackListPage token={token} />}
            path="/feedback"
          />
          <Route
            element={<AnalyticsPage token={token} />}
            path="/analytics"
          />
          <Route
            element={<VoiceHistoryPage token={token} />}
            path="/voice"
          />
          <Route
            element={
              <FeedbackPage
                sessionId={new URLSearchParams(window.location.search).get("session") ?? ""}
                token={token}
              />
            }
            path="/feedback/new"
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
