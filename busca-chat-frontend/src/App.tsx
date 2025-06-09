import React, { useState } from "react";
import "./App.css";

const API_BUSCA = "http://localhost:8000/buscar";
const API_CHAT = "http://localhost:5000/ask";

function App() {
  const [modo, setModo] = useState<"busca" | "chat">("busca");
  const [input, setInput] = useState("");
  const [respostas, setRespostas] = useState<string[]>([]);
  const [carregando, setCarregando] = useState(false);

  const enviar = async () => {
    if (!input.trim()) return;

    setCarregando(true);
    
    try {
      if (modo === "busca") {
        const response = await fetch(API_BUSCA, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: input, top_k: 3 }),
        });
        const data = await response.json();
        setRespostas(data);
      } else {
        const response = await fetch(API_CHAT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: input }),
        });
        const data = await response.json();
        setRespostas([data.response]);
      }
      setInput("");
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro ao processar requisição");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container">
      <h1>🔎 Busca Semântica & 🤖 Chatbot</h1>

      <select
        value={modo}
        onChange={(e) => {
          setModo(e.target.value as "busca" | "chat");
          setRespostas([]);
        }}
        disabled={carregando}
      >
        <option value="busca">Busca Semântica</option>
        <option value="chat">Chatbot</option>
      </select>

      {modo === "chat" && (
        <div id="suggestions">
          <strong>Dicas de perguntas:</strong>
          <ul>
            <li>Como instalo o programa X?</li>
            <li>Como faço login?</li>
            <li>Como alterar minha senha?</li>
            <li>Como sair do sistema?</li>
            <li>Quais os atalhos do sistema?</li>
          </ul>
        </div>
      )}

      <input
        type="text"
        placeholder="Digite sua pergunta..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !carregando && enviar()}
        disabled={carregando}
      />
      
      <button onClick={enviar} disabled={carregando || !input.trim()}>
        {carregando ? "Enviando..." : "Enviar"}
      </button>

      {carregando && <div className="loading">Processando...</div>}

      <div className="respostas">
        {respostas.map((resp, i) => (
          <div key={i} className="resposta">
            {resp}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;