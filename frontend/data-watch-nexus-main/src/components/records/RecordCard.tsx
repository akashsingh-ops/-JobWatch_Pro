import React from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Record } from '@/types/records';
import { ExternalLink, Calendar } from 'lucide-react';
import { motion } from 'framer-motion';

interface RecordCardProps {
  record: Record;
  onClick?: () => void;
}

export const RecordCard: React.FC<RecordCardProps> = ({ record, onClick }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const handleExternalClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(record.url, '_blank');
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <Card 
        className="h-full cursor-pointer card-hover group bg-gradient-to-br from-card to-card/80 border-0 shadow-md"
        onClick={onClick}
      >
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="font-semibold text-lg leading-tight line-clamp-2 group-hover:text-primary transition-colors">
                {record.title}
              </h3>
              <p className="text-sm text-muted-foreground mt-1">{record.source}</p>
            </div>
            <Badge 
              variant="secondary" 
              className="ml-2 bg-accent/10 text-accent hover:bg-accent/20"
            >
              {record.category}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="pt-0 space-y-4">
          <p className="text-sm text-muted-foreground line-clamp-3">
            {record.description}
          </p>

          <div className="flex items-center justify-between pt-2 border-t border-border/50">
            <div className="flex items-center text-xs text-muted-foreground">
              <Calendar className="h-3 w-3 mr-1" />
              {formatDate(record.publishedDate)}
            </div>

            <Button
              size="sm"
              variant="ghost"
              className="h-8 px-3 text-primary hover:text-primary-foreground hover:bg-primary"
              onClick={handleExternalClick}
            >
              <ExternalLink className="h-3 w-3 mr-1" />
              Open
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};