import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../lib/api";

type Props = {
  onLogin: (token: string, user: { display_name: string }) => void;
};

export default function LoginPage({ onLogin }: Props) {
  const navigate = useNavigate();
  const called = useRef(false);

  useEffect(() => {
    if (called.current) return;
    called.current = true;
    login()
      .then((payload) => {
        onLogin(payload.access_token, payload.user);
        navigate("/scenarios");
      })
      .catch(() => {});
  }, [onLogin, navigate]);

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Callibr</h1>
        <p className="login-subtitle">Simulation d'entretien client</p>
        <div className="login-spinner" />
        <p>Connexion en cours...</p>
      </div>
    </div>
  );
}
