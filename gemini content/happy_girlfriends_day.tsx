import React, { useState, useEffect } from 'react';
import { Heart, Sparkles, Stars, ArrowRight, Quote, HeartHandshake } from 'lucide-react';

const slides = [
  {
    id: 0,
    title: "Hey Neha...",
    subtitle: "I have a little surprise for you. ❤️",
    icon: Stars,
    actionText: "Tap to open",
  },
  {
    id: 1,
    title: "Happy Girlfriend's Day!",
    subtitle: "To the most beautiful, amazing, and perfect girl in the entire universe.",
    icon: Sparkles,
  },
  {
    id: 2,
    title: "You are my everything.",
    subtitle: "Every moment with you feels like magic. You're not just my girlfriend; you're my peace, my joy, and my whole world.",
    icon: HeartHandshake,
  },
  {
    id: 3,
    title: "To my adorable...",
    subtitle: "Bittu 🤌🏻",
    icon: Quote,
    highlight: true,
  },
  {
    id: 4,
    title: "I Love You.",
    subtitle: "More than words could ever explain. Thank you for being mine today, tomorrow, and forever.",
    icon: Heart,
    signature: "Forever yours, Saurabh ❤️"
  }
];

// Component for the floating background hearts
const FloatingHearts = () => {
  const [hearts, setHearts] = useState([]);

  useEffect(() => {
    // Generate random hearts
    const newHearts = Array.from({ length: 20 }).map((_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      animationDuration: `${Math.random() * 4 + 4}s`,
      animationDelay: `${Math.random() * 5}s`,
      size: Math.random() * 20 + 10,
    }));
    setHearts(newHearts);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {hearts.map((heart) => (
        <div
          key={heart.id}
          className="floating-heart absolute bottom-0 text-pink-300/40"
          style={{
            left: heart.left,
            animationDuration: heart.animationDuration,
            animationDelay: heart.animationDelay,
            fontSize: `${heart.size}px`,
          }}
        >
          <Heart fill="currentColor" stroke="none" />
        </div>
      ))}
    </div>
  );
};

export default function App() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const nextSlide = () => {
    if (currentSlide < slides.length - 1 && !isTransitioning) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentSlide(prev => prev + 1);
        setIsTransitioning(false);
      }, 400); // Wait for fade out
    }
  };

  const restart = () => {
    if (!isTransitioning) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentSlide(0);
        setIsTransitioning(false);
      }, 400);
    }
  };

  const slide = slides[currentSlide];
  const Icon = slide.icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-200 via-pink-400 to-red-500 flex items-center justify-center p-4 relative overflow-hidden font-sans">
      
      {/* CSS Animations */}
      <style>
        {`
          @keyframes floatUp {
            0% { transform: translateY(100vh) scale(0.5) rotate(0deg); opacity: 0; }
            20% { opacity: 0.8; }
            80% { opacity: 0.8; }
            100% { transform: translateY(-20vh) scale(1.5) rotate(45deg); opacity: 0; }
          }
          .floating-heart {
            animation: floatUp ease-in infinite;
          }
          
          @keyframes pulse-soft {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
          }
          .animate-pulse-soft {
            animation: pulse-soft 2s ease-in-out infinite;
          }
        `}
      </style>

      <FloatingHearts />

      {/* Main Card */}
      <div 
        className={`relative z-10 w-full max-w-lg transition-opacity duration-500 ${isTransitioning ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}`}
      >
        <div 
          onClick={nextSlide}
          className="bg-white/20 backdrop-blur-xl border border-white/30 p-8 md:p-12 rounded-3xl shadow-2xl flex flex-col items-center text-center cursor-pointer min-h-[400px] justify-center transform transition-transform hover:scale-[1.02]"
        >
          
          <div className={`mb-6 text-pink-100 p-4 rounded-full bg-white/10 ${slide.highlight ? 'animate-pulse-soft' : ''}`}>
            <Icon size={slide.highlight ? 64 : 48} strokeWidth={1.5} className={slide.highlight ? "text-red-500 fill-red-500" : "text-white"} />
          </div>

          <h1 className={`text-3xl md:text-5xl font-bold text-white mb-4 drop-shadow-md ${slide.highlight ? 'text-5xl md:text-7xl tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-red-200 to-red-500 drop-shadow-xl' : ''}`}>
            {slide.title}
          </h1>

          <p className={`text-lg md:text-xl text-pink-50 leading-relaxed font-medium drop-shadow-sm ${slide.highlight ? 'text-3xl mt-2 font-bold' : ''}`}>
            {slide.subtitle}
          </p>

          {slide.signature && (
            <p className="mt-8 text-xl text-white font-bold italic tracking-wide">
              {slide.signature}
            </p>
          )}

          {/* Navigation Controls */}
          <div className="mt-12 w-full flex justify-center">
            {currentSlide === 0 ? (
              <button 
                onClick={(e) => { e.stopPropagation(); nextSlide(); }}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-full transition-all backdrop-blur-md border border-white/40 font-semibold"
              >
                {slide.actionText} <ArrowRight size={20} />
              </button>
            ) : currentSlide < slides.length - 1 ? (
              <p className="text-pink-100/70 text-sm animate-pulse flex items-center gap-2">
                Tap anywhere to continue <ArrowRight size={16} />
              </p>
            ) : (
              <button 
                onClick={(e) => { e.stopPropagation(); restart(); }}
                className="flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-full transition-all backdrop-blur-md border border-white/40 font-semibold mt-4"
              >
                Read again <Heart size={18} fill="currentColor" />
              </button>
            )}
          </div>
          
        </div>
      </div>
      
      {/* Progress Dots */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center gap-2 z-20">
        {slides.map((_, index) => (
          <div 
            key={index} 
            className={`h-2 rounded-full transition-all duration-500 ${currentSlide === index ? 'w-8 bg-white' : 'w-2 bg-white/30'}`}
          />
        ))}
      </div>
    </div>
  );
}