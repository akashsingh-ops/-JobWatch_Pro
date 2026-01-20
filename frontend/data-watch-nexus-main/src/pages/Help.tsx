import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { 
  HelpCircle, 
  Mail, 
  MessageSquare, 
  Book, 
  Send,
  ExternalLink,
  Search,
  Phone,
  Clock
} from 'lucide-react';
import { motion } from 'framer-motion';

const Help: React.FC = () => {
  const { toast } = useToast();
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const faqs = [
    {
      id: '1',
      question: 'How do I set up email alerts for specific categories?',
      answer: 'Go to Settings > Preferences and select the categories you want to monitor. Toggle "Email Alerts" to ON in the Notifications tab. You can also set keywords for more specific filtering.'
    },
    {
      id: '2',
      question: 'How often are new records added to the system?',
      answer: 'Our system automatically fetches and processes new data records every 4 hours. You will receive notifications based on your alert preferences when new matching records are available.'
    },
    {
      id: '3',
      question: 'Can I export records to Excel or CSV format?',
      answer: 'Yes! On the Dashboard, use the search and filter options to find the records you want, then click the "Export" button. You can choose between CSV, Excel, or JSON formats.'
    },
    {
      id: '4',
      question: 'What is the daily digest and how do I control it?',
      answer: 'The daily digest is a summary email sent every morning with highlights of new records matching your interests. You can enable/disable it in Settings > Notifications and customize the time it\'s sent.'
    },
    {
      id: '5',
      question: 'How do I change my password or update account information?',
      answer: 'Visit your Profile page to update personal information like name and email. For password changes, click "Change Password" in the Security section and follow the prompts.'
    },
    {
      id: '6',
      question: 'Why am I not receiving email notifications?',
      answer: 'Check your Settings > Notifications to ensure email alerts are enabled. Also verify that our emails aren\'t going to your spam folder. Add our domain to your email whitelist for best delivery.'
    },
    {
      id: '7',
      question: 'Is there a mobile app available?',
      answer: 'Currently, Data Alerts is a web-based application optimized for mobile browsers. We\'re working on dedicated mobile apps for iOS and Android - stay tuned for updates!'
    },
    {
      id: '8',
      question: 'How can I delete my account and data?',
      answer: 'To delete your account, please contact our support team at support@dataalerts.com. We will permanently remove all your data within 30 days as per our privacy policy.'
    }
  ];

  const supportLinks = [
    {
      title: 'Documentation',
      description: 'Comprehensive guides and tutorials',
      icon: Book,
      url: '#',
      external: true
    },
    {
      title: 'Email Support',
      description: 'support@dataalerts.com',
      icon: Mail,
      url: 'mailto:support@dataalerts.com',
      external: true
    },
    {
      title: 'Live Chat',
      description: 'Available Mon-Fri, 9AM-5PM EST',
      icon: MessageSquare,
      url: '#',
      external: false
    }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!contactForm.name || !contactForm.email || !contactForm.message) {
      toast({
        title: 'Error',
        description: 'Please fill in all required fields',
        variant: 'destructive'
      });
      return;
    }

    // Simulate form submission
    setTimeout(() => {
      toast({
        title: 'Message sent!',
        description: 'We\'ll get back to you within 24 hours.'
      });
      
      setContactForm({
        name: '',
        email: '',
        subject: '',
        message: ''
      });
    }, 1000);
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold flex items-center justify-center gap-2 mb-4">
            <HelpCircle className="h-10 w-10 text-primary" />
            Help & Support
          </h1>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Find answers to common questions or get in touch with our support team
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {/* FAQ Section */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Frequently Asked Questions
                </CardTitle>
                <CardDescription>
                  Quick answers to the most common questions about Data Alerts
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Accordion type="single" collapsible className="w-full">
                  {faqs.map((faq, index) => (
                    <motion.div
                      key={faq.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                    >
                      <AccordionItem value={faq.id}>
                        <AccordionTrigger className="text-left">
                          {faq.question}
                        </AccordionTrigger>
                        <AccordionContent className="text-muted-foreground">
                          {faq.answer}
                        </AccordionContent>
                      </AccordionItem>
                    </motion.div>
                  ))}
                </Accordion>
              </CardContent>
            </Card>

            {/* Contact Form */}
            <Card className="mt-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" />
                  Contact Support
                </CardTitle>
                <CardDescription>
                  Can't find what you're looking for? Send us a message and we'll help you out.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="space-y-2">
                      <Label htmlFor="name">Name *</Label>
                      <Input
                        id="name"
                        value={contactForm.name}
                        onChange={(e) => setContactForm(prev => ({ ...prev, name: e.target.value }))}
                        placeholder="Your full name"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={contactForm.email}
                        onChange={(e) => setContactForm(prev => ({ ...prev, email: e.target.value }))}
                        placeholder="your@email.com"
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="subject">Subject</Label>
                    <Input
                      id="subject"
                      value={contactForm.subject}
                      onChange={(e) => setContactForm(prev => ({ ...prev, subject: e.target.value }))}
                      placeholder="Brief description of your issue"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="message">Message *</Label>
                    <Textarea
                      id="message"
                      value={contactForm.message}
                      onChange={(e) => setContactForm(prev => ({ ...prev, message: e.target.value }))}
                      placeholder="Describe your question or issue in detail..."
                      rows={5}
                      required
                    />
                  </div>
                  
                  <Button type="submit" className="w-full">
                    <Send className="h-4 w-4 mr-2" />
                    Send Message
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Support Links Sidebar */}
          <div className="space-y-6">
            {/* Quick Support Links */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Support</CardTitle>
                <CardDescription>
                  Get help through multiple channels
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {supportLinks.map((link, index) => (
                  <motion.div
                    key={link.title}
                    initial={{ opacity: 0, x: 10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <Button
                      variant="ghost"
                      className="w-full justify-start h-auto p-4"
                      asChild={link.external}
                    >
                      {link.external ? (
                        <a href={link.url} target="_blank" rel="noopener noreferrer">
                          <link.icon className="h-5 w-5 mr-3 text-primary" />
                          <div className="text-left">
                            <div className="font-medium">{link.title}</div>
                            <div className="text-xs text-muted-foreground">{link.description}</div>
                          </div>
                          {link.external && <ExternalLink className="h-4 w-4 ml-auto" />}
                        </a>
                      ) : (
                        <div>
                          <link.icon className="h-5 w-5 mr-3 text-primary" />
                          <div className="text-left">
                            <div className="font-medium">{link.title}</div>
                            <div className="text-xs text-muted-foreground">{link.description}</div>
                          </div>
                        </div>
                      )}
                    </Button>
                  </motion.div>
                ))}
              </CardContent>
            </Card>

            {/* Response Times */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Response Times
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Email Support</span>
                  <Badge variant="secondary">24 hours</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Live Chat</span>
                  <Badge variant="default">Instant</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Critical Issues</span>
                  <Badge variant="destructive">2 hours</Badge>
                </div>
              </CardContent>
            </Card>

            {/* Status */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">System Status</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm">All systems operational</span>
                </div>
                <Button variant="link" className="p-0 h-auto text-xs mt-2">
                  View status page
                  <ExternalLink className="h-3 w-3 ml-1" />
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Help;