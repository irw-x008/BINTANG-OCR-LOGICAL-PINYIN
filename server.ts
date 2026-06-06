import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json({ limit: "50mb" }));

  // API route for Fallback Test
  app.post("/api/fallback-test", async (req, res) => {
    const results = [];
    let success = false;
    let finalProvider = "";
    let finalText = "";

    try {
      // 1. Priority 1: Gemini
      if (process.env.GEMINI_API_KEY) {
        try {
          const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
          const response = await ai.models.generateContent({
            model: "gemini-2.5-flash",
            contents: "Balas dengan 'Koneksi Sukses! Saya siap membantu OCR'. Pura-pura Anda adalah sistem OCR Bintang Logic.",
          });
          results.push({ provider: "Gemini", status: "Success", text: response.text });
          success = true;
          finalProvider = "Gemini";
          finalText = response.text || "";
        } catch (e: any) {
          results.push({ provider: "Gemini", status: "Failed", error: e.message });
        }
      } else {
        results.push({ provider: "Gemini", status: "Skipped", error: "API Key Not Found" });
      }

      // 2. Priority 2: OpenRouter
      if (!success) {
        if (process.env.OPENROUTER_API_KEY) {
          try {
            const orRes = await fetch("https://openrouter.ai/api/v1/chat/completions", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                model: "qwen/qwen-2.5-vl-7b-instruct:free",
                messages: [{ role: "user", content: "Balas dengan 'Koneksi Sukses! Saya siap membantu OCR'." }]
              })
            });
            const data = await orRes.json();
            if (orRes.ok) {
              results.push({ provider: "OpenRouter", status: "Success", text: data.choices[0].message.content });
              success = true;
              finalProvider = "OpenRouter";
              finalText = data.choices[0].message.content;
            } else {
              results.push({ provider: "OpenRouter", status: "Failed", error: JSON.stringify(data.error || data) });
            }
          } catch (e: any) {
            results.push({ provider: "OpenRouter", status: "Failed", error: e.message });
          }
        } else {
          results.push({ provider: "OpenRouter", status: "Skipped", error: "API Key Not Found" });
        }
      }

      // 3. Priority 3: Groq
      if (!success) {
        if (process.env.GROQ_API_KEY) {
          try {
            const gRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${process.env.GROQ_API_KEY}`,
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                model: "llama-3.2-11b-vision-preview",
                messages: [{ role: "user", content: "Balas dengan 'Koneksi Sukses! Saya siap membantu OCR'." }]
              })
            });
            const data = await gRes.json();
            if (gRes.ok) {
              results.push({ provider: "Groq", status: "Success", text: data.choices[0].message.content });
              success = true;
              finalProvider = "Groq";
              finalText = data.choices[0].message.content;
            } else {
              results.push({ provider: "Groq", status: "Failed", error: JSON.stringify(data.error || data) });
            }
          } catch (e: any) {
            results.push({ provider: "Groq", status: "Failed", error: e.message });
          }
        } else {
          results.push({ provider: "Groq", status: "Skipped", error: "API Key Not Found" });
        }
      }

      res.json({ success, provider: finalProvider, text: finalText, logs: results });

    } catch (e: any) {
      res.status(500).json({ error: e.message, logs: results });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();
