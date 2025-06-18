import { useState } from "react";
import API from "../api";

const CreateGroup = ({ onGroupCreated }) => {
  const [groupName, setGroupName] = useState("");
  const [userNames, setUserNames] = useState(["", ""]); // start with 2 users

  const handleUserChange = (index, value) => {
    const updatedUsers = [...userNames];
    updatedUsers[index] = value;
    setUserNames(updatedUsers);
  };

  const addUserField = () => {
    setUserNames([...userNames, ""]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Create users
      const userIds = [];
      for (const name of userNames) {
        const res = await API.post("/users/", { name });
        userIds.push(res.data.id);
      }

      // Create group
      const res = await API.post("/groups/", {
        name: groupName,
        user_ids: userIds,
      });

      onGroupCreated(res.data); // pass data back to parent
    } catch (error) {
      alert("Error creating group");
      console.error(error);
    }
  };

  return (
    <div className="p-4 border rounded shadow max-w-md mx-auto">
      <h2 className="text-lg font-semibold mb-4">Create a New Group</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Group Name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          className="w-full p-2 border rounded mb-2"
          required
        />
        <h4 className="font-medium">Users:</h4>
        {userNames.map((name, i) => (
          <input
            key={i}
            type="text"
            placeholder={`User ${i + 1}`}
            value={name}
            onChange={(e) => handleUserChange(i, e.target.value)}
            className="w-full p-2 border rounded mb-2"
            required
          />
        ))}
        <button
          type="button"
          onClick={addUserField}
          className="text-blue-500 underline mb-3"
        >
          ➕ Add Another User
        </button>
        <br />
        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Create Group
        </button>
      </form>
    </div>
  );
};

export default CreateGroup;
