export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T | null;
  message: string | null;
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function queryGraph(question: string): Promise<ApiResponse<{ answer: string }>> {
  console.log('Mock: queryGraph', question);
  await sleep(1500);
  return {
    status: 'success',
    data: { answer: `This is a mock response for your question: "${question}". The UI is working in standalone mode without the Python backend.` },
    message: null
  };
}

export async function processCSV(): Promise<ApiResponse<{ task_id: string; message: string }>> {
  console.log('Mock: processCSV');
  await sleep(2000);
  return {
    status: 'success',
    data: { task_id: 'mock-csv-task-id', message: 'CSV processing started (Mock)' },
    message: null
  };
}

export async function processHTML(): Promise<ApiResponse<{ task_id: string; message: string }>> {
  console.log('Mock: processHTML');
  await sleep(2000);
  return {
    status: 'success',
    data: { task_id: 'mock-html-task-id', message: 'HTML processing started (Mock)' },
    message: null
  };
}

export async function healthCheck(): Promise<ApiResponse<{ neo4j_connected: boolean }>> {
  console.log('Mock: healthCheck');
  return {
    status: 'success',
    data: { neo4j_connected: true },
    message: null
  };
}
