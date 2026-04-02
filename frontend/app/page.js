"use client";
import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [model, setModel] = useState("llama3-8b");
  const [prompt, setPrompt] = useState("");
  const [maxTokens, setMaxTokens] = useState(100);
  const [taskId, setTaskId] = useState(null);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_URL}/tasks`);
      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.error("Failed to fetch tasks", err);
    }
  };

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model, prompt, max_tokens: maxTokens }),
      });
      const data = await res.json();
      setTaskId(data.task_id);
      setStatus(data.status);
    } catch (err) {
      console.error("Failed to submit", err);
    }
    setLoading(false);
  };

  const checkResult = async () => {
    if (!taskId) return;
    try {
      const res = await fetch(`${API_URL}/result/${taskId}`);
      const data = await res.json();
      setStatus(data.status);
      if (data.result) setResult(data.result);
    } catch (err) {
      console.error("Failed to fetch result", err);
    }
  };

  useEffect(() => {
    fetchTasks();
    const interval = setInterval(fetchTasks, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (taskId && status !== "completed") {
      const interval = setInterval(checkResult, 2000);
      return () => clearInterval(interval);
    }
  }, [taskId, status]);

  const getStatusColor = (s) => {
    switch (s) {
      case "completed": return "text-green-600";
      case "failed": return "text-red-600";
      case "processing": return "text-yellow-600";
      default: return "text-gray-600";
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">AI算力匹配桥</h1>
        
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">模型选择</label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="llama3-8b">Llama 3 8B</option>
              <option value="mistral-7b">Mistral 7B</option>
              <option value="qwen-7b">Qwen 7B</option>
            </select>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">输入Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full p-2 border rounded h-32"
              placeholder="输入你的问题..."
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Max Tokens: {maxTokens}</label>
            <input
              type="range"
              min="50"
              max="500"
              value={maxTokens}
              onChange={(e) => setMaxTokens(Number(e.target.value))}
              className="w-full"
            />
          </div>
          
          <button
            onClick={handleSubmit}
            disabled={loading || !prompt.trim()}
            className="bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50"
          >
            {loading ? "提交中..." : "提交任务"}
          </button>
        </div>
        
        {(taskId || result) && (
          <div className="bg-white p-6 rounded-lg shadow mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">当前任务</h2>
              <span className={`font-medium ${getStatusColor(status)}`}>
                {status}
              </span>
            </div>
            {taskId && <p className="text-sm text-gray-500">Task ID: {taskId}</p>}
            {result && (
              <div className="mt-4 p-4 bg-gray-100 rounded">
                <pre className="whitespace-pre-wrap">{result}</pre>
              </div>
            )}
          </div>
        )}
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">历史任务</h2>
          <div className="space-y-2">
            {tasks.map((task) => (
              <div key={task.task_id} className="p-3 border rounded flex justify-between items-center">
                <div>
                  <span className="font-medium">{task.model}</span>
                  <span className="text-gray-500 text-sm ml-2">
                    {task.prompt.substring(0, 30)}...
                  </span>
                </div>
                <span className={`text-sm ${getStatusColor(task.status)}`}>
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
