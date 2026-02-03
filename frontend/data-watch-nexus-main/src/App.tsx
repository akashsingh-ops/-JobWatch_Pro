import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider } from "@/components/theme/ThemeProvider";
import { Layout } from "@/components/layout/Layout";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import { apiUtils } from "@/api/client";
import Landing from "@/pages/Landing";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Dashboard from "@/pages/Dashboard";
import JobDetail from '@/pages/JobDetail';
import SavedJobs from '@/pages/SavedJobs';
import Settings from "@/pages/Settings";
import Notifications from "@/pages/Notifications";
import Profile from "@/pages/Profile";
import Activity from "@/pages/Activity";
import Help from "@/pages/Help";
import AdminDashboard from "@/pages/AdminDashboard";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        // Don't retry on 4xx errors (client errors)
        if (error?.response?.status >= 400 && error?.response?.status < 500) {
          return false;
        }
        // Retry up to 2 times for network/server errors
        return failureCount < 2;
      },
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: (failureCount, error: any) => {
        // Don't retry mutations on client errors
        if (error?.response?.status >= 400 && error?.response?.status < 500) {
          return false;
        }
        return failureCount < 1;
      },
      onError: (error: any) => {
        console.error('Mutation error:', error);
        // Global error handling for mutations
        if (apiUtils.isAuthError(error)) {
          // Handle auth errors globally
          console.warn('Authentication error in mutation');
        }
      },
    },
  },
});

const App = () => (
  <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="system" storageKey="data-alerts-theme">
        <TooltipProvider>
          <AuthProvider>
            <Toaster />
            <Sonner />
            <BrowserRouter>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              {/* Protected routes with layout */}
              <Route path="/dashboard" element={
                <Layout>
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/jobs/:id" element={
                <Layout>
                  <ProtectedRoute>
                    <JobDetail />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/saved-jobs" element={
                <Layout>
                  <ProtectedRoute>
                    <SavedJobs />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/notifications" element={
                <Layout>
                  <ProtectedRoute>
                    <Notifications />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/profile" element={
                <Layout>
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/activity" element={
                <Layout>
                  <ProtectedRoute>
                    <Activity />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/settings" element={
                <Layout>
                  <ProtectedRoute>
                    <Settings />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/help" element={
                <Layout>
                  <ProtectedRoute>
                    <Help />
                  </ProtectedRoute>
                </Layout>
              } />
              <Route path="/admin" element={
                <Layout>
                  <ProtectedRoute>
                    <AdminDashboard />
                  </ProtectedRoute>
                </Layout>
              } />
              
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
          </AuthProvider>
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </ErrorBoundary>
);

export default App;
