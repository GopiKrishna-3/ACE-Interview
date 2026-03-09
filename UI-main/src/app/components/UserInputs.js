"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:5000";

const ResumeUpload = ({ closeModal, setQuestions, setIsInterviewStarted }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [job_description, setJobDescription] = useState("");
  const [knowledgeDomain, setKnowledgeDomain] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleBrowseClick = () => {
    document.getElementById("fileInput").click();
  };

  const generateQuestions = (data) => {
    let allQuestions = [];
    const apiResponse = data.apiResponse || '';
    
    // Clean up markdown code fences
    const jsonString = apiResponse.replace(/^```json\n|\n```$/g, '').trim();

    try {
      const jsonData = JSON.parse(jsonString);

      // 1. Direct 'questions' array (New Format)
      if (jsonData && Array.isArray(jsonData.questions)) {
        allQuestions = jsonData.questions;
      } 
      // 2. Nested sections -> subsections (Old Format Fallback)
      else if (jsonData && Array.isArray(jsonData.sections)) {
        jsonData.sections.forEach((section) => {
          if (section.subsections && Array.isArray(section.subsections)) {
            section.subsections.forEach((subsection) => {
              if (subsection.questions && Array.isArray(subsection.questions)) {
                subsection.questions.forEach((q) => allQuestions.push(q));
              }
            });
          }
        });
      }
      // 3. Last resort: Find any array of strings in the object
      if (allQuestions.length === 0) {
        Object.values(jsonData).forEach(val => {
          if (Array.isArray(val) && val.length > 0 && typeof val[0] === 'string') {
            allQuestions = val;
          }
        });
      }
    } catch (error) {
      console.error("Error parsing JSON response from AI:", error);
    }

    if (allQuestions.length === 0) {
      console.warn("Could not find any questions in AI response. Response was:", apiResponse);
      alert("AI generated the questions but in a format we couldn't read. Please try again.");
    }
    
    setQuestions(allQuestions);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      alert("Please upload a resume.");
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("job_description", job_description);
      formData.append("knowledge_domain", knowledgeDomain);

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload data.");
      }

      const result = await response.json();
      console.log(result);
      generateQuestions(result);
      setIsInterviewStarted(true);
      closeModal();
    } catch (error) {
      console.error("Error uploading data:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-11/12 max-w-lg p-6 relative">
        <button
          onClick={closeModal}
          className="absolute top-3 right-3 text-gray-600 hover:text-gray-800"
        >
          ✖
        </button>
        <h1 className="text-2xl font-bold text-indigo-600 mb-4">AceAI</h1>
        <h2 className="text-xl font-semibold mb-6">Start Your Next Interview</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <h3 className="font-semibold text-lg text-gray-900">Resume</h3>
            <p className="text-sm text-gray-900 mb-2">Upload your resume (pdf)</p>
            <div className="border-2 border-dashed border-gray-400 rounded-md p-4 flex items-center justify-between">
                <span className="text-black text-sm font-medium">
                  {selectedFile ? selectedFile.name : "Drag & Drop File"}
                </span>
              <button
                type="button"
                onClick={handleBrowseClick}
                className="bg-indigo-600 text-white py-1 px-3 rounded-md hover:bg-indigo-700 transition"
              >
                Browse File
              </button>
              <input
                id="fileInput"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-lg text-gray-900">Job Description</h3>
            <textarea
              placeholder="Add job description"
              value={job_description}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full border border-gray-400 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent text-black placeholder-gray-700"
            ></textarea>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-lg text-gray-900">Mention Knowledge Domain</h3>
            <input
              type="text"
              placeholder="E.g., AI, ML, Web Dev"
              value={knowledgeDomain}
              onChange={(e) => setKnowledgeDomain(e.target.value)}
              className="w-full border border-gray-400 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent text-black placeholder-gray-700"
            />
          </div>

          <button
            type="submit"
            disabled={isUploading}
            className={`${
              isUploading ? "bg-gray-400" : "bg-indigo-600 hover:bg-indigo-700"
            } text-white py-2 px-4 rounded-md transition w-full`}
          >
            {isUploading ? "Uploading..." : "Launch"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResumeUpload;