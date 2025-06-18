import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import API from "../api";

const GroupPage = () => {
  const { groupId } = useParams();
  const [group, setGroup] = useState(null);
  const [balances, setBalances] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resGroup = await API.get(`/groups/${groupId}`);
        setGroup(resGroup.data);

        const resBalances = await API.get(`/groups/${groupId}/balances`);
        setBalances(resBalances.data);
      } catch (err) {
        console.error("Error fetching group data", err);
      }
    };

    fetchData();
  }, [groupId]);

  if (!group) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-2">{group.name}</h1>
      <p className="mb-4">{group.users.length} Members</p>

      <h2 className="text-xl font-semibold mt-6 mb-2">Balances</h2>
      {balances.length === 0 ? (
        <p>No balances to display</p>
      ) : (
        <ul className="list-disc ml-6">
          {balances.map((bal, i) => (
            <li key={i}>
              User {bal.from_user_id} owes User {bal.to_user_id}: ₹{bal.amount}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GroupPage;
