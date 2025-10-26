"""
YouTube SEO Analyzer - Main Application
Advanced tool for analyzing YouTube videos and suggesting SEO tags
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from youtube_analyzer import YouTubeAnalyzer
from seo_engine import SEOEngine
from trend_analyzer import TrendAnalyzer
import json

class YouTubeSEOAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced YouTube SEO Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize analyzers
        self.youtube_analyzer = YouTubeAnalyzer()
        self.seo_engine = SEOEngine()
        self.trend_analyzer = TrendAnalyzer()
        
        # Current analysis data
        self.current_video_data = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="YouTube SEO Analyzer", 
                               font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#FF0000')
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.url_entry = ttk.Entry(url_frame, width=80, font=('Arial', 10))
        self.url_entry.grid(row=0, column=0, padx=5)
        
        self.analyze_btn = ttk.Button(url_frame, text="Analyze Video", 
                                       command=self.analyze_video)
        self.analyze_btn.grid(row=0, column=1, padx=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(2, weight=1)
        
        # Tab 1: Video Analysis
        self.analysis_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_tab, text="Video Analysis")
        self.setup_analysis_tab()
        
        # Tab 2: SEO Suggestions
        self.seo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.seo_tab, text="SEO Suggestions")
        self.setup_seo_tab()
        
        # Tab 3: Trend Analysis
        self.trend_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.trend_tab, text="Trend Analysis")
        self.setup_trend_tab()
        
        # Tab 4: Performance Metrics
        self.metrics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.metrics_tab, text="Performance Metrics")
        self.setup_metrics_tab()
        
        # Tab 5: Settings
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
    def setup_analysis_tab(self):
        """Setup video analysis tab"""
        # Video info section
        info_frame = ttk.LabelFrame(self.analysis_tab, text="Video Information", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.analysis_tab.rowconfigure(0, weight=1)
        self.analysis_tab.columnconfigure(0, weight=1)
        
        self.video_info_text = scrolledtext.ScrolledText(info_frame, width=80, height=35, 
                                                          font=('Arial', 10), wrap=tk.WORD)
        self.video_info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.rowconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        
    def setup_seo_tab(self):
        """Setup SEO suggestions tab"""
        # Suggested tags
        tags_frame = ttk.LabelFrame(self.seo_tab, text="Suggested Tags", padding="10")
        tags_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.suggested_tags_text = scrolledtext.ScrolledText(tags_frame, width=80, height=10, 
                                                              font=('Arial', 10), wrap=tk.WORD)
        self.suggested_tags_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Copy tags button
        copy_btn = ttk.Button(tags_frame, text="Copy Tags", command=self.copy_tags)
        copy_btn.grid(row=1, column=0, pady=5)
        
        # Optimization suggestions
        opt_frame = ttk.LabelFrame(self.seo_tab, text="Optimization Suggestions", padding="10")
        opt_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.seo_tab.rowconfigure(1, weight=1)
        
        self.optimization_text = scrolledtext.ScrolledText(opt_frame, width=80, height=15, 
                                                            font=('Arial', 10), wrap=tk.WORD)
        self.optimization_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        opt_frame.rowconfigure(0, weight=1)
        opt_frame.columnconfigure(0, weight=1)
        
    def setup_trend_tab(self):
        """Setup trend analysis tab"""
        # Trending topics
        trending_frame = ttk.LabelFrame(self.trend_tab, text="Related Trending Topics", padding="10")
        trending_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.trending_text = scrolledtext.ScrolledText(trending_frame, width=80, height=12, 
                                                        font=('Arial', 10), wrap=tk.WORD)
        self.trending_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Trend-based suggestions
        suggestions_frame = ttk.LabelFrame(self.trend_tab, text="Trend-Based Tag Suggestions", padding="10")
        suggestions_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        self.trend_tab.rowconfigure(1, weight=1)
        
        self.trend_suggestions_text = scrolledtext.ScrolledText(suggestions_frame, width=80, height=12, 
                                                                 font=('Arial', 10), wrap=tk.WORD)
        self.trend_suggestions_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        suggestions_frame.rowconfigure(0, weight=1)
        suggestions_frame.columnconfigure(0, weight=1)
        
    def setup_metrics_tab(self):
        """Setup performance metrics tab"""
        metrics_frame = ttk.Frame(self.metrics_tab, padding="10")
        metrics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.metrics_tab.rowconfigure(0, weight=1)
        self.metrics_tab.columnconfigure(0, weight=1)
        
        # SEO Score
        score_frame = ttk.LabelFrame(metrics_frame, text="Overall SEO Score", padding="10")
        score_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.seo_score_label = tk.Label(score_frame, text="--/100", 
                                        font=('Arial', 48, 'bold'), fg='#4CAF50')
        self.seo_score_label.grid(row=0, column=0)
        
        # Detailed metrics
        details_frame = ttk.LabelFrame(metrics_frame, text="Detailed Metrics", padding="10")
        details_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        metrics_frame.rowconfigure(1, weight=1)
        
        self.metrics_text = scrolledtext.ScrolledText(details_frame, width=80, height=20, 
                                                       font=('Arial', 10), wrap=tk.WORD)
        self.metrics_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_frame.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        
    def setup_settings_tab(self):
        """Setup settings tab"""
        settings_frame = ttk.Frame(self.settings_tab, padding="10")
        settings_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Performance metric weights
        weights_frame = ttk.LabelFrame(settings_frame, text="Performance Metric Weights", padding="10")
        weights_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.weight_vars = {}
        metrics = [
            ("Title Optimization", "title_weight", 20),
            ("Description Quality", "description_weight", 15),
            ("Tag Relevance", "tag_weight", 25),
            ("Content Quality", "content_weight", 20),
            ("Trend Alignment", "trend_weight", 20)
        ]
        
        for i, (label, var_name, default) in enumerate(metrics):
            ttk.Label(weights_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            var = tk.IntVar(value=default)
            self.weight_vars[var_name] = var
            scale = ttk.Scale(weights_frame, from_=0, to=100, variable=var, orient=tk.HORIZONTAL, length=200)
            scale.grid(row=i, column=1, padx=5, pady=5)
            value_label = ttk.Label(weights_frame, text=f"{default}%")
            value_label.grid(row=i, column=2, padx=5, pady=5)
            var.trace_add('write', lambda *args, vl=value_label, v=var: vl.config(text=f"{v.get()}%"))
        
        # Number of tags to suggest
        tags_frame = ttk.LabelFrame(settings_frame, text="Tag Settings", padding="10")
        tags_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(tags_frame, text="Number of tags to suggest:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_tags_var = tk.IntVar(value=30)
        tags_spinbox = ttk.Spinbox(tags_frame, from_=10, to=50, textvariable=self.num_tags_var, width=10)
        tags_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        # Trend analysis settings
        trend_frame = ttk.LabelFrame(settings_frame, text="Trend Analysis Settings", padding="10")
        trend_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(trend_frame, text="Trend region:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.region_var = tk.StringVar(value="US")
        region_combo = ttk.Combobox(trend_frame, textvariable=self.region_var, 
                                     values=["US", "GB", "CA", "AU", "IN", "WORLD"], width=15)
        region_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(trend_frame, text="Timeframe:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.timeframe_var = tk.StringVar(value="7d")
        timeframe_combo = ttk.Combobox(trend_frame, textvariable=self.timeframe_var, 
                                        values=["1d", "7d", "30d", "90d"], width=15)
        timeframe_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Save settings button
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.grid(row=3, column=0, pady=10)
        
    def analyze_video(self):
        """Analyze the YouTube video"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        # Disable analyze button during analysis
        self.analyze_btn.config(state='disabled')
        self.status_var.set("Analyzing video...")
        
        # Run analysis in separate thread
        thread = threading.Thread(target=self._perform_analysis, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _perform_analysis(self, url):
        """Perform the actual analysis (runs in separate thread)"""
        try:
            # Extract video data
            self.update_status("Extracting video data...")
            video_data = self.youtube_analyzer.analyze_video(url)
            self.current_video_data = video_data
            
            # Display video information
            self.root.after(0, self.display_video_info, video_data)
            
            # Analyze SEO
            self.update_status("Analyzing SEO...")
            seo_results = self.seo_engine.analyze_seo(video_data)
            self.root.after(0, self.display_seo_results, seo_results)
            
            # Analyze trends
            self.update_status("Analyzing trends...")
            trend_results = self.trend_analyzer.analyze_trends(
                video_data, 
                region=self.region_var.get(),
                timeframe=self.timeframe_var.get()
            )
            self.root.after(0, self.display_trend_results, trend_results)
            
            # Calculate metrics
            self.update_status("Calculating performance metrics...")
            metrics = self.calculate_metrics(video_data, seo_results, trend_results)
            self.root.after(0, self.display_metrics, metrics)
            
            self.update_status("Analysis complete!")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Analysis failed: {str(e)}")
            self.update_status("Analysis failed")
        finally:
            self.root.after(0, lambda: self.analyze_btn.config(state='normal'))
    
    def update_status(self, message):
        """Update status bar"""
        self.root.after(0, self.status_var.set, message)
    
    def display_video_info(self, video_data):
        """Display video information"""
        self.video_info_text.delete(1.0, tk.END)
        
        info = f"""Title: {video_data.get('title', 'N/A')}

Video ID: {video_data.get('video_id', 'N/A')}

Channel: {video_data.get('channel', 'N/A')}

Views: {video_data.get('views', 'N/A'):,}

Likes: {video_data.get('likes', 'N/A'):,}

Upload Date: {video_data.get('upload_date', 'N/A')}

Duration: {video_data.get('duration', 'N/A')}

Description:
{video_data.get('description', 'N/A')}

Current Tags:
{', '.join(video_data.get('tags', [])) if video_data.get('tags') else 'No tags available'}

Transcript Summary:
{video_data.get('transcript_summary', 'Transcript not available')}
"""
        self.video_info_text.insert(1.0, info)
        
    def display_seo_results(self, seo_results):
        """Display SEO analysis results"""
        # Suggested tags
        self.suggested_tags_text.delete(1.0, tk.END)
        tags = seo_results.get('suggested_tags', [])
        tags_text = ', '.join(tags[:self.num_tags_var.get()])
        self.suggested_tags_text.insert(1.0, tags_text)
        
        # Optimization suggestions
        self.optimization_text.delete(1.0, tk.END)
        suggestions = seo_results.get('suggestions', [])
        for i, suggestion in enumerate(suggestions, 1):
            self.optimization_text.insert(tk.END, f"{i}. {suggestion}\n\n")
            
    def display_trend_results(self, trend_results):
        """Display trend analysis results"""
        # Trending topics
        self.trending_text.delete(1.0, tk.END)
        trending = trend_results.get('trending_topics', [])
        for i, topic in enumerate(trending, 1):
            self.trending_text.insert(tk.END, f"{i}. {topic['name']} (Score: {topic['score']})\n")
        
        # Trend-based suggestions
        self.trend_suggestions_text.delete(1.0, tk.END)
        trend_tags = trend_results.get('trend_tags', [])
        for i, tag_info in enumerate(trend_tags, 1):
            self.trend_suggestions_text.insert(tk.END, 
                f"{i}. {tag_info['tag']} - {tag_info['reason']}\n\n")
    
    def display_metrics(self, metrics):
        """Display performance metrics"""
        # Overall score
        score = metrics.get('overall_score', 0)
        self.seo_score_label.config(text=f"{score}/100")
        
        # Color code the score
        if score >= 80:
            color = '#4CAF50'  # Green
        elif score >= 60:
            color = '#FFC107'  # Yellow
        else:
            color = '#F44336'  # Red
        self.seo_score_label.config(fg=color)
        
        # Detailed metrics
        self.metrics_text.delete(1.0, tk.END)
        
        details = f"""Overall SEO Score: {score}/100

Individual Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title Optimization: {metrics.get('title_score', 0)}/100
{metrics.get('title_feedback', '')}

Description Quality: {metrics.get('description_score', 0)}/100
{metrics.get('description_feedback', '')}

Tag Relevance: {metrics.get('tag_score', 0)}/100
{metrics.get('tag_feedback', '')}

Content Quality: {metrics.get('content_score', 0)}/100
{metrics.get('content_feedback', '')}

Trend Alignment: {metrics.get('trend_score', 0)}/100
{metrics.get('trend_feedback', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendations:
"""
        for i, rec in enumerate(metrics.get('recommendations', []), 1):
            details += f"{i}. {rec}\n"
        
        self.metrics_text.insert(1.0, details)
    
    def calculate_metrics(self, video_data, seo_results, trend_results):
        """Calculate performance metrics"""
        metrics = {}
        
        # Get weights
        weights = {key: var.get() for key, var in self.weight_vars.items()}
        
        # Title score
        title_score = seo_results.get('title_score', 0)
        metrics['title_score'] = title_score
        metrics['title_feedback'] = seo_results.get('title_feedback', '')
        
        # Description score
        description_score = seo_results.get('description_score', 0)
        metrics['description_score'] = description_score
        metrics['description_feedback'] = seo_results.get('description_feedback', '')
        
        # Tag score
        tag_score = seo_results.get('tag_score', 0)
        metrics['tag_score'] = tag_score
        metrics['tag_feedback'] = seo_results.get('tag_feedback', '')
        
        # Content score
        content_score = seo_results.get('content_score', 0)
        metrics['content_score'] = content_score
        metrics['content_feedback'] = seo_results.get('content_feedback', '')
        
        # Trend score
        trend_score = trend_results.get('trend_score', 0)
        metrics['trend_score'] = trend_score
        metrics['trend_feedback'] = trend_results.get('trend_feedback', '')
        
        # Calculate weighted overall score
        total_weight = sum(weights.values())
        if total_weight > 0:
            overall_score = (
                title_score * weights['title_weight'] +
                description_score * weights['description_weight'] +
                tag_score * weights['tag_weight'] +
                content_score * weights['content_weight'] +
                trend_score * weights['trend_weight']
            ) / total_weight
        else:
            overall_score = 0
        
        metrics['overall_score'] = int(overall_score)
        metrics['recommendations'] = seo_results.get('recommendations', [])
        
        return metrics
    
    def copy_tags(self):
        """Copy suggested tags to clipboard"""
        tags_text = self.suggested_tags_text.get(1.0, tk.END).strip()
        if tags_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(tags_text)
            messagebox.showinfo("Success", "Tags copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No tags to copy")
    
    def save_settings(self):
        """Save settings to file"""
        settings = {
            'weights': {key: var.get() for key, var in self.weight_vars.items()},
            'num_tags': self.num_tags_var.get(),
            'region': self.region_var.get(),
            'timeframe': self.timeframe_var.get()
        }
        
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            
            # Load weights
            for key, value in settings.get('weights', {}).items():
                if key in self.weight_vars:
                    self.weight_vars[key].set(value)
            
            # Load other settings
            self.num_tags_var.set(settings.get('num_tags', 30))
            self.region_var.set(settings.get('region', 'US'))
            self.timeframe_var.set(settings.get('timeframe', '7d'))
        except FileNotFoundError:
            pass  # No settings file yet
        except Exception as e:
            print(f"Error loading settings: {e}")

def main():
    root = tk.Tk()
    app = YouTubeSEOAnalyzer(root)
    app.load_settings()
    root.mainloop()

if __name__ == "__main__":
    main()

