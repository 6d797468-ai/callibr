import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../lib/api";
import ErrorPanel from "../components/ErrorPanel";
import { friendlyError, type UserFacingError } from "../lib/errors";

type Props = {
  onLogin: (token: string, user: { display_name: string }) => void;
};

export default function LoginPage({ onLogin }: Props) {
  const navigate = useNavigate();
  const [error, setError] = useState<UserFacingError | null>(null);
  const onLoginRef = useRef(onLogin);
  onLoginRef.current = onLogin;

  const doLogin = useCallback(() => {
    setError(null);
    login()
      .then((payload) => {
        onLoginRef.current(payload.access_token, payload.user);
        navigate("/scenarios");
      })
      .catch((err) => setError(friendlyError(err)));
  }, [navigate]);

  useEffect(() => {
    doLogin();
  }, [doLogin]);

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Callibr</h1>
        <p className="login-subtitle">Simulation d'entretien client</p>
        {error ? (
          <ErrorPanel error={error} onRetry={doLogin} />
        ) : (
          <>
            <div className="login-spinner" />
            <p>Connexion en cours...</p>
          </>
        )}
      </div>
    </div>
  );
}
