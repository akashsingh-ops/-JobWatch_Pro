import React from 'react';
import { Job } from '@/types/jobs';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Building2, 
  MapPin, 
  DollarSign, 
  Clock, 
  Bookmark, 
  BookmarkCheck, 
  ExternalLink,
  Sparkles
} from 'lucide-react';

interface JobCardProps {
  job: Job;
  onClick?: () => void;
  onSave?: (e: React.MouseEvent) => void;
}

export const JobCard: React.FC<JobCardProps> = ({ job, onClick, onSave }) => {
  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      const now = new Date();
      const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 3600 * 24));
      if (diffInDays === 0) return 'Today';
      if (diffInDays === 1) return '1 day ago';
      if (diffInDays < 7) return `${diffInDays} days ago`;
      return date.toLocaleDateString();
    } catch {
      return 'Recently';
    }
  };

  return (
    <Card 
      onClick={onClick}
      className={`group cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-primary/40 relative overflow-hidden flex flex-col justify-between h-full ${
        job.featured ? 'border-primary/30 bg-primary/[0.02]' : ''
      }`}
    >
      {job.featured && (
        <div className="absolute top-0 right-0">
          <div className="bg-primary text-primary-foreground text-[10px] font-semibold px-2 py-0.5 rounded-bl-md flex items-center gap-1 shadow-sm">
            <Sparkles className="h-2.5 w-2.5" /> Featured
          </div>
        </div>
      )}

      <CardContent className="p-5 flex flex-col justify-between flex-1">
        <div>
          {/* Header */}
          <div className="flex items-start justify-between gap-2 mb-3">
            <div className="flex-1 pr-6">
              <h3 className="font-semibold text-base leading-snug group-hover:text-primary transition-colors line-clamp-1">
                {job.title}
              </h3>
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground mt-1">
                <Building2 className="h-3.5 w-3.5 shrink-0" />
                <span className="font-medium text-foreground/80 line-clamp-1">{job.company}</span>
              </div>
            </div>
            
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 shrink-0 text-muted-foreground hover:text-primary transition-colors -mr-2 -mt-1"
              onClick={(e) => {
                e.stopPropagation();
                if (onSave) onSave(e);
              }}
              title={job.saved ? 'Remove bookmark' : 'Save job'}
            >
              {job.saved ? (
                <BookmarkCheck className="h-4 w-4 text-primary fill-primary/20" />
              ) : (
                <Bookmark className="h-4 w-4" />
              )}
            </Button>
          </div>

          {/* Description */}
          <p className="text-xs text-muted-foreground line-clamp-2 mb-4 leading-relaxed">
            {job.description}
          </p>

          {/* Badges and details */}
          <div className="flex flex-wrap items-center gap-1.5 mb-4">
            <Badge variant="secondary" className="text-[11px] font-normal py-0">
              {job.category}
            </Badge>
            <Badge variant="outline" className="text-[11px] font-normal py-0">
              {job.type}
            </Badge>
            {job.experienceLevel && (
              <Badge variant="outline" className="text-[11px] font-normal py-0 border-muted-foreground/30">
                {job.experienceLevel}
              </Badge>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-border/50 flex items-center justify-between text-xs text-muted-foreground mt-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              <MapPin className="h-3 w-3 text-muted-foreground" />
              <span className="truncate max-w-[110px]">{job.location}</span>
            </div>
            {job.salary && (
              <div className="flex items-center gap-0.5 text-foreground/90 font-medium">
                <DollarSign className="h-3 w-3 text-emerald-500 shrink-0" />
                <span>{job.salary.split(' - ')[0]}</span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-1 text-[11px]">
            <Clock className="h-3 w-3" />
            <span>{formatDate(job.postedDate)}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
