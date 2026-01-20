import React from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Job } from '@/types/jobs';
import { 
  MapPin, 
  Calendar, 
  DollarSign, 
  ExternalLink, 
  Heart, 
  Briefcase,
  Building2
} from 'lucide-react';
import { motion } from 'framer-motion';

interface JobCardProps {
  job: Job;
  onClick: () => void;
  onSave?: () => void;
}

export const JobCard: React.FC<JobCardProps> = ({ job, onClick, onSave }) => {
  const formatSalary = (salary: Job['salary']) => {
    if (!salary) return null;
    const { min, max, currency } = salary;
    if (min && max) {
      return `${currency}${min.toLocaleString()} - ${currency}${max.toLocaleString()}`;
    }
    return min ? `From ${currency}${min.toLocaleString()}` : null;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffInDays === 0) return 'Today';
    if (diffInDays === 1) return 'Yesterday';
    if (diffInDays < 7) return `${diffInDays} days ago`;
    if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`;
    return date.toLocaleDateString();
  };

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <Card 
        className="cursor-pointer border-0 shadow-md hover:shadow-xl transition-all duration-300 bg-gradient-to-br from-card to-card/80 h-full"
        onClick={onClick}
      >
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3 flex-1">
              <Avatar className="h-12 w-12">
                <AvatarImage src={job.companyLogo} alt={job.company} />
                <AvatarFallback>
                  <Building2 className="h-6 w-6" />
                </AvatarFallback>
              </Avatar>
              
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-lg line-clamp-2 text-foreground group-hover:text-primary transition-colors">
                  {job.title}
                </h3>
                <p className="text-muted-foreground font-medium">{job.company}</p>
                
                <div className="flex items-center text-sm text-muted-foreground mt-1">
                  <MapPin className="h-3 w-3 mr-1" />
                  <span className="truncate">{job.location}</span>
                  {job.remote && (
                    <Badge variant="secondary" className="ml-2 text-xs">
                      Remote
                    </Badge>
                  )}
                </div>
              </div>
            </div>
            
            {onSave && (
              <Button
                variant="ghost"
                size="sm"
                className="shrink-0 h-8 w-8 p-0"
                onClick={(e) => {
                  e.stopPropagation();
                  onSave();
                }}
              >
                <Heart 
                  className={`h-4 w-4 ${job.saved ? 'fill-primary text-primary' : 'text-muted-foreground'}`} 
                />
              </Button>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Job Details */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center text-muted-foreground">
                <Briefcase className="h-3 w-3 mr-1" />
                <span>{job.type}</span>
              </div>
              
              {job.salary && (
                <div className="flex items-center text-primary font-medium">
                  <DollarSign className="h-3 w-3 mr-1" />
                  <span className="text-xs">{formatSalary(job.salary)}</span>
                </div>
              )}
            </div>
            
            <div className="flex items-center text-sm text-muted-foreground">
              <Calendar className="h-3 w-3 mr-1" />
              <span>Posted {formatDate(job.postedDate)}</span>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-1">
            {job.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
            {job.tags.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{job.tags.length - 3}
              </Badge>
            )}
          </div>

          {/* Description Preview */}
          <p className="text-sm text-muted-foreground line-clamp-2">
            {job.description}
          </p>

          {/* Actions */}
          <div className="pt-2 flex items-center justify-between">
            <Button
              variant="ghost"
              size="sm"
              className="text-primary hover:text-primary-hover"
              onClick={(e) => {
                e.stopPropagation();
                onClick();
              }}
            >
              View Details
              <ExternalLink className="ml-1 h-3 w-3" />
            </Button>
            
            {job.featured && (
              <Badge className="bg-gradient-to-r from-primary to-primary-glow text-primary-foreground">
                Featured
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};