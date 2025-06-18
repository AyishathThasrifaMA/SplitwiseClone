import { useEffect, useState } from "react";
import API from "../api";
import CreateGroup from "../components/CreateGroup";

const HomePage = () => {
  const [groups, setGroups] = useState([]);
  const [showForm, setShowForm] = useState(false);

  const fetchGroups = async () => {
    try {
      const res = await API.get("/users/1/balances");
      console.log(res.data);
    } catch (error) {
      console.error("Error fetching balances", error);
    }
  };

  const handleGroupCreated = (newGroup) => {
    setGroups([...groups, newGroup]);
    setShowForm(false);
  };

  useEffect(() => {
    // Add real data fetching here
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-800">💬 Your Groups</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 hover:bg-blue-700 transition text-white px-4 py-2 rounded-lg shadow-md"
          >
            ➕ Create Group
          </button>
        </div>

        {showForm && (
          <div className="mb-8 border border-gray-200 bg-white p-6 rounded-xl shadow-sm">
            <CreateGroup onGroupCreated={handleGroupCreated} />
          </div>
        )}

        {groups.length === 0 ? (
          <div className="text-center text-gray-500 mt-12 italic">
            No groups created yet. Start by creating one!
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {groups.map((group) => (
              <div
                key={group.id}
                className="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-all duration-200"
              >
                <h2 className="text-xl font-semibold text-gray-800 mb-2">
                  {group.name}
                </h2>
                <p className="text-sm text-gray-500 mb-3">
                  👥 {group.users.length} member{group.users.length !== 1 ? "s" : ""}
                </p>
                <a
                  href={`/groups/${group.id}`}
                  className="inline-block text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  ➡️ View Group
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
