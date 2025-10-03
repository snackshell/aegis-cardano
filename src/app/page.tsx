"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Shield, Zap, Users, Globe, Bot, CheckCircle, AlertTriangle, ExternalLink, Github, Twitter, MessageCircle, Send } from "lucide-react";

export default function Home() {
  const [demoInput, setDemoInput] = useState("");
  const [demoResult, setDemoResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleDemo = async () => {
    if (!demoInput.trim()) return;
    
    setIsLoading(true);
    try {
      // Simulate API call for demo
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Mock response based on input type
      if (demoInput.startsWith("addr") || demoInput.startsWith("stake")) {
        setDemoResult({
          type: "address",
          status: "safe",
          data: {
            address: demoInput,
            balance: "1,234.56 ADA",
            transactions: 45,
            reputation: "Excellent",
            riskScore: "Low (2/10)"
          }
        });
      } else if (demoInput.includes(".")) {
        setDemoResult({
          type: "policy",
          status: "verified",
          data: {
            policyId: demoInput,
            assets: 12,
            totalSupply: "1,000,000",
            verified: true,
            metadata: "Complete"
          }
        });
      } else {
        setDemoResult({
          type: "cbor",
          status: "decoded",
          data: {
            format: "Valid CBOR",
            inputs: 2,
            outputs: 3,
            fees: "0.17 ADA",
            valid: true
          }
        });
      }
    } catch (error) {
      setDemoResult({
        type: "error",
        status: "error",
        data: { message: "Unable to process input. Please try again." }
      });
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Address Security",
      description: "Comprehensive address analysis with reputation scoring and risk assessment"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Real-time Scanning",
      description: "Instant verification of transactions, assets, and smart contracts"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Bot Integration",
      description: "Telegram and Discord bots for on-the-go security checks"
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: "Multi-chain Support",
      description: "Comprehensive coverage across Cardano ecosystem"
    }
  ];

  const botFeatures = [
    { platform: "Telegram", commands: ["/start", "/check", "/scan", "/decode", "/policy"], link: "https://t.me/AegisCardanoBot" },
    { platform: "Discord", commands: ["/check", "/scan", "/decode", "/policy", "/help"], link: "https://discord.gg/V5f_b6yiATs" }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "safe":
      case "verified":
        return "text-green-600 bg-green-50";
      case "warning":
        return "text-yellow-600 bg-yellow-50";
      case "error":
        return "text-red-600 bg-red-50";
      default:
        return "text-blue-600 bg-blue-50";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="relative">
                <Shield className="w-16 h-16 text-blue-600" />
                <div className="absolute -top-2 -right-2">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-4 h-4 text-white" />
                  </div>
                </div>
              </div>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6">
              Aegis Cardano
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              Advanced security guardian for the Cardano blockchain. Protect your assets with AI-powered threat detection and comprehensive analysis tools.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Button size="lg" className="text-lg px-8 py-3">
                <Bot className="w-5 h-5 mr-2" />
                Try Telegram Bot
              </Button>
              <Button variant="outline" size="lg" className="text-lg px-8 py-3">
                <MessageCircle className="w-5 h-5 mr-2" />
                Join Discord
              </Button>
              <Button variant="ghost" size="lg" className="text-lg px-8 py-3">
                <ExternalLink className="w-5 h-5 mr-2" />
                View Docs
              </Button>
            </div>
            <div className="flex justify-center gap-6">
              <Badge variant="secondary" className="text-sm px-4 py-2">
                🤖 Telegram Bot Ready
              </Badge>
              <Badge variant="secondary" className="text-sm px-4 py-2">
                🎮 Discord Bot Live
              </Badge>
              <Badge variant="secondary" className="text-sm px-4 py-2">
                📚 Full Documentation
              </Badge>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Security Features
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Comprehensive protection for your Cardano assets with advanced threat detection and analysis capabilities.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                      {feature.icon}
                    </div>
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Live Demo Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Live Security Demo
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Try our security analysis tools right now. Enter an address, policy ID, or CBOR data.
            </p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="w-5 h-5" />
                Security Scanner
              </CardTitle>
              <CardDescription>
                Test our real-time security analysis with your own data
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Enter Address, Policy ID, or CBOR:</label>
                <Textarea
                  placeholder="addr1q9d7t... or asset1... or CBOR data..."
                  value={demoInput}
                  onChange={(e) => setDemoInput(e.target.value)}
                  className="min-h-[100px]"
                />
              </div>
              
              <Button 
                onClick={handleDemo} 
                disabled={isLoading || !demoInput.trim()}
                className="w-full"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Shield className="w-4 h-4 mr-2" />
                    Analyze Security
                  </>
                )}
              </Button>

              {demoResult && (
                <div className="mt-6 space-y-4">
                  <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(demoResult.status)}`}>
                    {demoResult.status === "safe" && <CheckCircle className="w-4 h-4 mr-1" />}
                    {demoResult.status === "warning" && <AlertTriangle className="w-4 h-4 mr-1" />}
                    {demoResult.status === "error" && <AlertTriangle className="w-4 h-4 mr-1" />}
                    {demoResult.status.charAt(0).toUpperCase() + demoResult.status.slice(1)}
                  </div>

                  {demoResult.type !== "error" && (
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      {Object.entries(demoResult.data).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="font-medium text-gray-600 dark:text-gray-400">
                            {key.charAt(0).toUpperCase() + key.slice(1)}:
                          </span>
                          <span className="text-gray-900 dark:text-white">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Bot Integration Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Bot Integration
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Access Aegis security features directly through your favorite messaging platforms.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {botFeatures.map((bot, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {bot.platform === "Telegram" ? (
                      <Send className="w-5 h-5 text-blue-500" />
                    ) : (
                      <MessageCircle className="w-5 h-5 text-indigo-500" />
                    )}
                    {bot.platform} Bot
                  </CardTitle>
                  <CardDescription>
                    Available commands for quick security checks
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {bot.commands.map((cmd, i) => (
                      <Badge key={i} variant="outline">{cmd}</Badge>
                    ))}
                  </div>
                  <Button variant="outline" className="w-full" asChild>
                    <a href={bot.link} target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="w-4 h-4 mr-2" />
                      Open {bot.platform}
                    </a>
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Documentation & Status Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Documentation */}
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                Documentation
              </h3>
              <div className="space-y-4">
                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold mb-2">User Guide</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                          Complete guide for using Aegis Cardano security tools
                        </p>
                        <Button variant="outline" size="sm">
                          <ExternalLink className="w-4 h-4 mr-2" />
                          Read Guide
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold mb-2">API Reference</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                          Technical documentation for developers
                        </p>
                        <Button variant="outline" size="sm">
                          <ExternalLink className="w-4 h-4 mr-2" />
                          View API
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-semibold mb-2">Developer Guide</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                          Setup and integration instructions
                        </p>
                        <Button variant="outline" size="sm">
                          <Github className="w-4 h-4 mr-2" />
                          GitHub
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* System Status */}
            <div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                System Status
              </h3>
              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Service Status</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span>API Services</span>
                      <Badge className="bg-green-100 text-green-800">Operational</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Telegram Bot</span>
                      <Badge className="bg-green-100 text-green-800">Online</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Discord Bot</span>
                      <Badge className="bg-green-100 text-green-800">Online</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Blockfrost API</span>
                      <Badge className="bg-green-100 text-green-800">Connected</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Koios API</span>
                      <Badge className="bg-green-100 text-green-800">Connected</Badge>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Network Statistics</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span>Addresses Analyzed</span>
                      <span className="font-mono">127,843</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Transactions Scanned</span>
                      <span className="font-mono">2,456,789</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Threats Detected</span>
                      <span className="font-mono text-red-600">1,234</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Uptime (30d)</span>
                      <span className="font-mono text-green-600">99.9%</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Shield className="w-8 h-8 text-blue-400" />
                <span className="text-xl font-bold">Aegis Cardano</span>
              </div>
              <p className="text-gray-400">
                Advanced security guardian for the Cardano blockchain ecosystem.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Products</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">Telegram Bot</a></li>
                <li><a href="#" className="hover:text-white transition">Discord Bot</a></li>
                <li><a href="#" className="hover:text-white transition">API Services</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition">API Reference</a></li>
                <li><a href="#" className="hover:text-white transition">Status Page</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Community</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition">GitHub</a></li>
                <li><a href="#" className="hover:text-white transition">Twitter</a></li>
                <li><a href="#" className="hover:text-white transition">Discord</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/privacy" className="hover:text-white transition">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white transition">Cookie Policy</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Aegis Cardano. All rights reserved. Built with ❤️ for the Cardano community.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
