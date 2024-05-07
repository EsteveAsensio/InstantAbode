export interface OdooAuthResponse {
    jsonrpc: string;
    result?: {
      session_id: string;
      uid: number;
    };
    error?: {
      code: number;
      message: string;
      data: {
        name: string;
        message: string;
      };
    };
  }
  