import { createContext, useContext, useState, ReactNode } from "react";
import type { UserRole, MockUser } from "@/data/mockData";
import { mockUsers } from "@/data/mockData";

interface AuthContextType {
  user: MockUser | null;
  role: UserRole | null;
  login: (role: UserRole) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<MockUser | null>(() => {
    // Check if role is stored in sessionStorage
    const storedRole = sessionStorage.getItem("learniq_role") as UserRole | null;
    return storedRole ? mockUsers[storedRole] : null;
  });

  const login = (role: UserRole) => {
    sessionStorage.setItem("learniq_role", role);
    setUser(mockUsers[role]);
  };

  const logout = () => {
    sessionStorage.removeItem("learniq_role");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, role: user?.role ?? null, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
