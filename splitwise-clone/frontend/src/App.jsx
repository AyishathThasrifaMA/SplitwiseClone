import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import GroupPage from "./pages/GroupPage";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-blue-600 text-white p-4 text-center shadow">
          <h1 className="text-2xl font-bold">Splitwise Clone</h1>
        </header>
        <main className="p-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/groups/:groupId" element={<GroupPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
