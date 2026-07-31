import { ApiError } from "./types";

export type UserFacingError = {
  title: string;
  explanation: string;
  action: string;
  retryable: boolean;
};

const RETRY_LABEL = "Réessayer";

const UNEXPECTED: UserFacingError = {
  title: "Une erreur inattendue est survenue",
  explanation:
    "L'opération n'a pas pu aboutir. Merci de réessayer dans quelques instants.",
  action:
    "Réessayez ; si le problème persiste, contactez l'administrateur de Callibr.",
  retryable: true,
};

const NETWORK: UserFacingError = {
  title: "Connexion impossible",
  explanation:
    "Callibr ne parvient pas à joindre le serveur. Vérifiez votre connexion internet puis réessayez.",
  action: "Vérifiez votre connexion, puis cliquez sur « Réessayer ».",
  retryable: true,
};

const TIMEOUT: UserFacingError = {
  title: "Le serveur met trop de temps à répondre",
  explanation:
    "L'opération a pris plus de temps que prévu et a été interrompue.",
  action: "Cliquez sur « Réessayer » pour relancer l'opération.",
  retryable: true,
};

const SERVICE_UNAVAILABLE: UserFacingError = {
  title: "Service momentanément indisponible",
  explanation:
    "Le serveur a répondu de façon inattendue. Merci de réessayer dans quelques instants.",
  action: "Réessayez dans quelques instants.",
  retryable: true,
};

const LLM_UNAVAILABLE: UserFacingError = {
  title: "Service d'IA indisponible",
  explanation:
    "Le service d'intelligence artificielle est momentanément indisponible. Votre simulation n'a pas été perdue.",
  action: "Réessayez dans quelques instants.",
  retryable: true,
};

const DATASTORE_UNAVAILABLE: UserFacingError = {
  title: "Service de données indisponible",
  explanation:
    "Les données de Callibr sont momentanément inaccessibles.",
  action: "Réessayez dans quelques instants.",
  retryable: true,
};

const REPORT_UNAVAILABLE: UserFacingError = {
  title: "Rapport indisponible",
  explanation:
    "La génération du rapport a échoué. Merci de réessayer.",
  action: "Réessayez dans quelques instants.",
  retryable: true,
};

const SCENARIO_NOT_FOUND: UserFacingError = {
  title: "Scénario introuvable",
  explanation:
    "Ce scénario n'existe plus ou n'est plus disponible.",
  action: "Retournez à la liste des scénarios pour en choisir un autre.",
  retryable: false,
};

const NOT_FOUND: UserFacingError = {
  title: "Élément introuvable",
  explanation:
    "L'élément demandé n'existe plus ou n'est plus disponible.",
  action: "Retournez à l'écran précédent ou réessayez.",
  retryable: false,
};

const AUTH_EXPIRED: UserFacingError = {
  title: "Session expirée",
  explanation:
    "Votre session a expiré. Reconnectez-vous pour continuer.",
  action: "Reconnectez-vous.",
  retryable: false,
};

function httpError(err: ApiError): UserFacingError {
  const code = err.code ?? "";
  const payload = err.payload;
  if (payload.title && payload.explanation) {
    return {
      title: payload.title,
      explanation: payload.explanation,
      action: payload.action ?? "Réessayez.",
      retryable:
        payload.retryable ??
        (err.httpStatus !== null && err.httpStatus >= 500),
    };
  }
  if (code === "SCENARIO_NOT_FOUND") return SCENARIO_NOT_FOUND;
  if (code === "REPORT_UNAVAILABLE") return REPORT_UNAVAILABLE;
  if (code === "DATASTORE_UNAVAILABLE") return DATASTORE_UNAVAILABLE;
  if (code === "llm_error") return LLM_UNAVAILABLE;
  if (err.httpStatus === 401) return AUTH_EXPIRED;
  if (err.httpStatus === 404) return NOT_FOUND;
  if (err.httpStatus === 503) return SERVICE_UNAVAILABLE;
  return {
    ...UNEXPECTED,
    retryable:
      payload.retryable ??
      (err.httpStatus !== null && err.httpStatus >= 500),
  };
}

export function friendlyError(err: unknown): UserFacingError {
  if (err instanceof ApiError) {
    switch (err.causeType) {
      case "timeout":
        return TIMEOUT;
      case "network":
        return NETWORK;
      case "parse":
        return SERVICE_UNAVAILABLE;
      case "http":
        return httpError(err);
    }
  }
  return UNEXPECTED;
}

export { RETRY_LABEL };
