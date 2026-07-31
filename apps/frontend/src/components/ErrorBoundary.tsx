import { Component, type ErrorInfo, type ReactNode } from "react";
import ErrorPanel from "./ErrorPanel";
import { friendlyError } from "../lib/errors";

type Props = {
  children: ReactNode;
};

type State = {
  error: unknown;
  resetKey: number;
};

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null, resetKey: 0 };

  static getDerivedStateFromError(error: unknown): Partial<State> {
    return { error };
  }

  componentDidCatch(error: unknown, info: ErrorInfo) {
    console.error("ErrorBoundary caught:", error, info);
  }

  render() {
    if (this.state.error) {
      return (
        <div className="error-boundary">
          <ErrorPanel
            error={friendlyError(this.state.error)}
            onRetry={() =>
              this.setState((s) => ({
                error: null,
                resetKey: s.resetKey + 1,
              }))
            }
          />
        </div>
      );
    }
    return <div className="error-boundary-wrap" key={this.state.resetKey}>{this.props.children}</div>;
  }
}
