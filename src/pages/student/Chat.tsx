import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { chapters, mockChatHistory } from "@/data/mockData";
import { Send, Mic, Book, ChevronDown } from "lucide-react";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  citations?: { chapter: number; name: string; page: number }[];
};

export default function StudentChat() {
  const [messages, setMessages] = useState<Message[]>(mockChatHistory);
  const [input, setInput] = useState("");
  const [selectedChapter, setSelectedChapter] = useState<number | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: Message = {
      id: `u${Date.now()}`,
      role: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const aiMsg: Message = {
        id: `a${Date.now()}`,
        role: "assistant",
        content:
          "That's a great question! Based on your NCERT textbook, I found the following information:\n\n**Key Points:**\n1. This concept is covered in detail in your syllabus.\n2. Understanding the fundamentals will help you in your exams.\n3. Practice the related questions at the end of the chapter.\n\nWould you like me to explain any specific part in more detail?",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        citations: [
          { chapter: selectedChapter || 1, name: chapters[(selectedChapter || 1) - 1].name, page: 15 },
        ],
      };
      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)]">
      {/* Sidebar: Chapter selector */}
      <div className="hidden lg:flex w-64 flex-col border-r bg-background">
        <div className="p-4 border-b">
          <h3 className="font-semibold text-sm text-foreground">Select Chapter</h3>
          <p className="text-xs text-muted-foreground mt-1">Focus your questions</p>
        </div>
        <ScrollArea className="flex-1 p-2">
          <div className="space-y-1">
            <Button
              variant={selectedChapter === null ? "secondary" : "ghost"}
              className="w-full justify-start text-sm h-auto py-2 px-3"
              onClick={() => setSelectedChapter(null)}
            >
              <Book className="h-4 w-4 mr-2 shrink-0" />
              <span className="truncate">All Chapters</span>
            </Button>
            {chapters.map((ch) => (
              <Button
                key={ch.id}
                variant={selectedChapter === ch.id ? "secondary" : "ghost"}
                className="w-full justify-start text-sm h-auto py-2 px-3"
                onClick={() => setSelectedChapter(ch.id)}
              >
                <span className="shrink-0 w-6 text-muted-foreground">Ch {ch.id}</span>
                <span className="truncate">{ch.name}</span>
              </Button>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat header */}
        <div className="flex items-center justify-between border-b px-4 py-3 bg-background">
          <div>
            <h2 className="font-semibold text-foreground">Ask LearnIQ</h2>
            <p className="text-xs text-muted-foreground">
              {selectedChapter
                ? `Focused on: Chapter ${selectedChapter} — ${chapters[selectedChapter - 1].name}`
                : "Ask about any topic in your syllabus"}
            </p>
          </div>
          <Badge variant="outline" className="bg-accent/10 text-accent border-accent">
            NCERT Grade 8 Science
          </Badge>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4" ref={scrollRef}>
          <div className="max-w-3xl mx-auto space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <Card
                  className={`max-w-[85%] ${
                    msg.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-card"
                  }`}
                >
                  <CardContent className="p-3">
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {msg.citations.map((cite, idx) => (
                          <Badge
                            key={idx}
                            variant="secondary"
                            className="text-xs bg-accent/20 text-accent-foreground"
                          >
                            📖 Ch {cite.chapter}: {cite.name} (p.{cite.page})
                          </Badge>
                        ))}
                      </div>
                    )}
                    <p
                      className={`text-xs mt-2 ${
                        msg.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
                      }`}
                    >
                      {msg.timestamp}
                    </p>
                  </CardContent>
                </Card>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <Card className="bg-card">
                  <CardContent className="p-3">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "0ms" }} />
                      <span className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "150ms" }} />
                      <span className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Input area */}
        <div className="border-t p-4 bg-background">
          <div className="max-w-3xl mx-auto flex gap-2">
            <Button variant="outline" size="icon" className="shrink-0" title="Voice input (coming soon)">
              <Mic className="h-4 w-4" />
            </Button>
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question in Hindi or English..."
              className="flex-1"
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <Button onClick={handleSend} disabled={!input.trim()} className="bg-accent text-accent-foreground hover:bg-accent/90">
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-xs text-center text-muted-foreground mt-2">
            Answers are grounded in your NCERT textbook and cite the source chapter.
          </p>
        </div>
      </div>
    </div>
  );
}
