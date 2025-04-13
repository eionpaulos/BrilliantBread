import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload, Zap, FileImage, Save, ArrowLeft } from "lucide-react";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState("");
  const [generatedDiagram, setGeneratedDiagram] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAnalysisResult(""); // Reset analysis
      setGeneratedDiagram(null); // Reset diagram
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAnalysisResult(""); // Reset analysis
      setGeneratedDiagram(null); // Reset diagram
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;
    
    setIsAnalyzing(true);
    
    // Simulate processing delay
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowResults(true);
      
      // Mock analysis result
      setAnalysisResult(
        "Circuit analysis complete. This appears to be a simple voltage divider circuit with two resistors (R1: 10kΩ, R2: 5kΩ) connected to a 9V power source. The output voltage at the midpoint would be approximately 3V. The circuit also includes a capacitor (C1: 100μF) for filtering."
      );
      
      // Mock generated diagram
      setGeneratedDiagram(`
        9V
         |
         R1 (10kΩ)
         |
         +--- Output (3V)
         |
         R2 (5kΩ)
         |
        GND
      `);
    }, 2000);
  };

  const goBack = () => {
    setShowResults(false);
  };

  // Landing Page - Upload Screen
  if (!showResults) {
    return (
      <main className="flex-1 w-full min-h-screen bg-gray-50 flex items-center justify-center p-4 md:p-8 font-sans">
        <div className="w-full max-w-lg mx-auto">
          {/* Logo and Title */}
          <div className="flex items-center justify-center gap-3 mb-8">
            <span className="text-4xl md:text-5xl">🔌</span>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-gray-800">
              CircuLens
            </h1>
          </div>
          
          <p className="text-center text-gray-600 mb-10">
            Upload a circuit image to analyze its components and generate a clean diagram
          </p>

          {/* Upload Card */}
          <Card className="shadow-lg bg-white mb-6">
            <CardContent className="p-6">
              <div 
                className="border-2 border-dashed rounded-lg p-10 text-center cursor-pointer hover:bg-gray-50 transition-colors"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => document.getElementById("file-upload").click()}
              >
                <FileImage className="mx-auto h-16 w-16 text-gray-400 mb-4" />
                <p className="text-gray-700 mb-2 font-medium">Drag and drop your circuit image here</p>
                <p className="text-sm text-gray-500 mb-4">or click to browse your files</p>
                <p className="text-xs text-gray-400">Supports PNG, JPG, GIF up to 10MB</p>
                <input 
                  id="file-upload" 
                  type="file" 
                  className="hidden" 
                  accept="image/*" 
                  onChange={handleImageChange} 
                />
              </div>
            </CardContent>
          </Card>

          {/* Preview and Analyze */}
          {previewUrl && (
            <Card className="shadow-md bg-white overflow-hidden">
              <CardHeader className="pb-2 bg-gray-50">
                <CardTitle className="text-lg font-semibold text-gray-800">Selected Image</CardTitle>
              </CardHeader>
              <CardContent className="p-4">
                <div className="relative aspect-video mb-4">
                  <img
                    src={previewUrl}
                    alt="Uploaded circuit"
                    className="w-full h-full object-contain bg-white"
                  />
                </div>
                <div className="flex justify-center">
                  <Button 
                    className="w-full md:w-auto flex items-center justify-center gap-2 px-8 py-2" 
                    disabled={isAnalyzing}
                    onClick={handleAnalyze}
                    size="lg"
                  >
                    {isAnalyzing ? (
                      <>
                        <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Zap className="w-5 h-5" />
                        Analyze Circuit
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    );
  }

  // Results Page
  return (
    <main className="flex-1 w-full min-h-screen bg-gray-50 p-4 md:p-8 font-sans">
      <div className="w-full max-w-7xl mx-auto">
        {/* Header with fixed layout - using the responsive fix */}
        <div className="max-w-6xl mx-auto mb-10 flex flex-col md:flex-row justify-between items-start md:items-center">
          {/* Left: Back + Logo */}
          <div className="flex items-center mb-4 md:mb-0">
            <Button 
              variant="ghost" 
              className="w-10 h-10 mr-4 p-0 flex items-center justify-center bg-white rounded-lg shadow-sm"
              onClick={goBack}
              aria-label="Go back"
            >
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <span className="text-3xl mr-3">🔌</span>
            <h1 className="text-3xl font-bold tracking-tight text-gray-800">
              CircuLens
            </h1>
          </div>
          {/* Right: Upload New Image Button */}
          <Button
            variant="ghost"
            className="bg-white shadow-sm rounded-md px-5 py-2 flex items-center font-medium text-gray-800"
            onClick={() => {
              setSelectedImage(null);
              setPreviewUrl(null);
              setShowResults(false);
            }}
          >
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 4V16M12 4L8 8M12 4L16 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M20 16V20C20 21.1046 19.1046 22 18 22H6C4.89543 22 4 21.1046 4 20V16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Upload New Image
          </Button>
        </div>

        {/* Results Grid */}
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Original Circuit */}
            <Card className="shadow-md overflow-hidden">
              <CardHeader className="pb-2 bg-gray-50">
                <CardTitle className="text-lg font-semibold text-gray-800">Original Circuit</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                {previewUrl && (
                  <div className="relative aspect-video">
                    <img
                      src={previewUrl}
                      alt="Uploaded circuit"
                      className="w-full h-full object-contain bg-white p-2"
                    />
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Generated Circuit Diagram */}
            <Card className="shadow-md overflow-hidden">
              <CardHeader className="pb-2 bg-gray-50 flex flex-row justify-between items-center">
                <CardTitle className="text-lg font-semibold text-gray-800">Generated Circuit Diagram</CardTitle>
                {generatedDiagram && (
                  <Button variant="outline" size="sm" className="flex items-center gap-1">
                    <Save className="w-4 h-4" /> Export
                  </Button>
                )}
              </CardHeader>
              <CardContent className="p-0">
                {generatedDiagram ? (
                  <div className="bg-white p-4 aspect-video overflow-auto font-mono text-sm">
                    <pre>{generatedDiagram}</pre>
                  </div>
                ) : (
                  <div className="aspect-video flex items-center justify-center bg-gray-100 text-gray-400 text-sm p-4">
                    Circuit diagram will appear here after analysis
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Analysis Results */}
          <Card className="shadow-md bg-white">
            <CardHeader className="pb-2 bg-gray-50">
              <CardTitle className="text-lg font-semibold text-gray-800">Circuit Analysis</CardTitle>
            </CardHeader>
            <CardContent className="p-4">
              {isAnalyzing ? (
                <div className="flex items-center justify-center p-8">
                  <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mr-3"></div>
                  <p className="text-gray-600">Analyzing circuit components...</p>
                </div>
              ) : analysisResult ? (
                <div className="text-gray-700 p-2">{analysisResult}</div>
              ) : (
                <div className="text-gray-400 text-center p-8">
                  Analysis results will appear here after processing the image
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}

export default App;