import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<string>("");

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    // Placeholder: In real app, send to backend
    setAnalysisResult("Analyzing image using AI... (fake response)");
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6 space-y-6 bg-gray-100">
      <h1 className="text-3xl font-bold text-center">🔌 Circuit Analyzer</h1>

      <Card className="w-full max-w-md space-y-4 p-4">
        <Input type="file" accept="image/*" onChange={handleImageChange} />

        {previewUrl && (
          <img
            src={previewUrl}
            alt="Uploaded circuit"
            className="w-full rounded-md border shadow-md"
          />
        )}

        <Button disabled={!selectedImage} onClick={handleAnalyze}>
          Analyze Circuit
        </Button>
      </Card>

      {analysisResult && (
        <Card className="w-full max-w-md">
          <CardContent className="p-4">
            <p>{analysisResult}</p>
          </CardContent>
        </Card>
      )}
    </main>
  );
}

export default App;
