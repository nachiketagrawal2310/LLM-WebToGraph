export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T | null;
  message: string | null;
}

const BASE_URL = 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    return {
      status: 'error',
      data: null,
      message: errorData.message || `HTTP error! status: ${response.status}`
    };
  }
  return await response.json();
}

export async function queryGraph(question: string): Promise<ApiResponse<{ answer: string }>> {
  try {
    const response = await fetch(`${BASE_URL}/query_graph/${encodeURIComponent(question)}`);
    return await handleResponse<{ answer: string }>(response);
  } catch (error) {
    return {
      status: 'error',
      data: null,
      message: error instanceof Error ? error.message : 'Unknown connection error'
    };
  }
}

export async function processCSV(): Promise<ApiResponse<{ task_id: string; message: string }>> {
  try {
    const response = await fetch(`${BASE_URL}/generate_tags_from_csv`);
    return await handleResponse<{ task_id: string; message: string }>(response);
  } catch (error) {
    return {
      status: 'error',
      data: null,
      message: error instanceof Error ? error.message : 'Unknown connection error'
    };
  }
}

export async function processHTML(): Promise<ApiResponse<{ task_id: string; message: string }>> {
  try {
    const response = await fetch(`${BASE_URL}/generate_tags_from_html`);
    return await handleResponse<{ task_id: string; message: string }>(response);
  } catch (error) {
    return {
      status: 'error',
      data: null,
      message: error instanceof Error ? error.message : 'Unknown connection error'
    };
  }
}

export async function healthCheck(): Promise<ApiResponse<{ neo4j_connected: boolean }>> {
  try {
    const response = await fetch(`${BASE_URL}/health`);
    const data = await response.json();
    
    // Normalize health check response
    return {
      status: data.status === 'healthy' ? 'success' : 'error',
      data: { neo4j_connected: data.neo4j_connected || false },
      message: null
    };
  } catch (error) {
    return {
      status: 'error',
      data: { neo4j_connected: false },
      message: error instanceof Error ? error.message : 'Backend unreachable'
    };
  }
}
