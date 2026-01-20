export interface User {
  id: string;
  email: string;
  name: string;
  preferences?: {
    categories: string[];
    keywords: string[];
    emailNotifications: boolean;
  };
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<User>;
  register: (email: string, password: string, name: string) => Promise<User>;
  logout: () => void;
  loading: boolean;
  isAuthenticated: boolean;
}