import React from 'react';
import { HelpCircle, BookOpen, ShieldCheck, Terminal, Download, FileText, CheckCircle2, Server, Layers, Cpu } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';

const Help: React.FC = () => {
  const { toast } = useToast();

  const handlePrintPdf = () => {
    window.print();
  };

  const handleDownloadDoc = () => {
    fetch('/PROJECT_DOCUMENTATION.md')
      .then((res) => {
        if (!res.ok) throw new Error('File not found');
        return res.text();
      })
      .then((text) => {
        const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'JobWatch_Pro_End_to_End_Architecture_Doc.md';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        toast({
          title: 'Documentation Exported',
          description: 'The end-to-end documentation markdown has been downloaded.',
        });
      })
      .catch(() => {
        toast({
          title: 'Export Action',
          description: 'Use the Print to PDF button below or check PROJECT_DOCUMENTATION.md in root directory.',
        });
      });
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-8 max-w-4xl print:p-0 print:max-w-full">
      {/* Header */}
      <div className="border-b pb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <HelpCircle className="h-6 w-6 text-primary" />
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">System Documentation & Help</h1>
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            End-to-end technical reference, architecture documentation, and system guidelines.
          </p>
        </div>
        <div className="flex items-center gap-2 print:hidden">
          <Button variant="outline" size="sm" onClick={handleDownloadDoc} className="gap-1.5">
            <Download className="h-4 w-4" /> Download Markdown
          </Button>
          <Button size="sm" onClick={handlePrintPdf} className="gap-1.5">
            <FileText className="h-4 w-4" /> Save / Print as PDF
          </Button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border shadow-sm">
          <CardContent className="p-5 space-y-2">
            <div className="flex items-center gap-2 text-primary font-semibold text-sm">
              <Layers className="h-4 w-4" /> Frontend Stack
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              React 18, TypeScript, Tailwind CSS, Lucide Icons, Radix UI Primitives, next-themes.
            </p>
          </CardContent>
        </Card>

        <Card className="border shadow-sm">
          <CardContent className="p-5 space-y-2">
            <div className="flex items-center gap-2 text-primary font-semibold text-sm">
              <Cpu className="h-4 w-4" /> State & Caching
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              TanStack React Query v5 caching layer with optimistic mutations and local storage fallback.
            </p>
          </CardContent>
        </Card>

        <Card className="border shadow-sm">
          <CardContent className="p-5 space-y-2">
            <div className="flex items-center gap-2 text-primary font-semibold text-sm">
              <Server className="h-4 w-4" /> Network & API
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Centralized Axios client with automatic Bearer JWT interceptors and 401 recovery.
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main End-to-End Specification Document */}
      <Card className="border shadow-md">
        <CardHeader className="border-b bg-muted/30 pb-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" /> End-to-End System Specifications
            </CardTitle>
            <span className="text-xs text-muted-foreground font-mono bg-background px-2.5 py-1 rounded border">v1.0.0</span>
          </div>
        </CardHeader>
        <CardContent className="p-6 space-y-6 text-sm text-foreground/90 leading-relaxed">
          <section className="space-y-2">
            <h2 className="text-base font-bold text-foreground">1. Executive Overview</h2>
            <p className="text-xs text-muted-foreground leading-relaxed">
              JobWatch Pro is a high-performance career telemetry and job opportunity aggregation platform. It delivers real-time job filtering across tech specializations (Full Stack, AI/ML, DevOps, Cloud, Product), customizable alert triggers, candidate telemetry tracking, and administrative listing controls.
            </p>
          </section>

          <section className="space-y-2">
            <h2 className="text-base font-bold text-foreground">2. Architecture & Data Flow</h2>
            <div className="bg-muted/40 rounded-lg p-4 font-mono text-xs text-muted-foreground overflow-x-auto space-y-1">
              <p>[React UI Views & Pages]</p>
              <p>       ↓</p>
              <p>[TanStack Query & AuthContext]</p>
              <p>       ↓</p>
              <p>[Axios HTTP Client + Local Storage Engine (`jobwatch_jobs`)]</p>
            </div>
          </section>

          <section className="space-y-3">
            <h2 className="text-base font-bold text-foreground">3. Core Application Modules</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="border rounded p-3 bg-background">
                <p className="font-semibold text-foreground mb-1">/dashboard & /jobs/:id</p>
                <p className="text-muted-foreground">Multi-criteria search, categories (Engineering, Data/AI, DevOps), salary ranges, and direct application links.</p>
              </div>
              <div className="border rounded p-3 bg-background">
                <p className="font-semibold text-foreground mb-1">/saved</p>
                <p className="text-muted-foreground">User-curated job bookmarks with real-time optimistic state mutations and query invalidation.</p>
              </div>
              <div className="border rounded p-3 bg-background">
                <p className="font-semibold text-foreground mb-1">/notifications & /activity</p>
                <p className="text-muted-foreground">Alert configurations, real-time alert feed, candidate application telemetry, and performance metric charts.</p>
              </div>
              <div className="border rounded p-3 bg-background">
                <p className="font-semibold text-foreground mb-1">/admin</p>
                <p className="text-muted-foreground">Admin/recruiter posting portal to publish new opportunities, set experience tags, and manage active roles.</p>
              </div>
            </div>
          </section>

          <section className="space-y-2">
            <h2 className="text-base font-bold text-foreground">4. Technical Specifications</h2>
            <ul className="text-xs text-muted-foreground space-y-1.5 list-disc list-inside">
              <li><strong className="text-foreground">Authentication:</strong> JWT Bearer token support in AuthContext with automatic mock session failover for development sandboxes.</li>
              <li><strong className="text-foreground">Persistence:</strong> High-reliability client-side storage engine ensuring bookmarking and job creation persist across page reloads.</li>
              <li><strong className="text-foreground">Styling & Theming:</strong> HSL-based CSS variables supporting seamless dark mode, light mode, and system preference switching.</li>
            </ul>
          </section>
        </CardContent>
      </Card>
    </div>
  );
};

export default Help;
