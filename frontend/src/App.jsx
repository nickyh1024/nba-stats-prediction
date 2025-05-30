import React, { useEffect, useState } from "react";
import { players } from "./players";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const load = async () => {
      const all = await Promise.all(
        players.map(async (player) => {
          const res = await fetch("http://localhost:5050/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ features: player.features }),
          });
          const json = await res.json();
          return {
            ...player,
            ...Object.fromEntries(
              Object.entries(json).map(([key, val]) => [key, parseFloat(val.toFixed(3))])
            ),
          };
        })
      );
  
      // ✅ Sort by predicted points
      all.sort((a, b) => b.pts - a.pts);
  
      setData(all);
    };
  
    load();
  }, []);
  
  

  const getColor = (value) => {
    const num = parseFloat(value);
    if (num >= 25) return "bg-green-200 text-green-800";
    if (num >= 18) return "bg-yellow-100 text-yellow-700";
    return "bg-red-200 text-red-800";
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold mb-6">NBA Stat Prediction Dashboard</h1>
      <div className="overflow-x-auto bg-white shadow-md rounded-lg">
        <table className="min-w-full text-sm">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Age</th>
            <th>MPG</th>
            <th>FG%</th>
            <th>FT%</th>
            <th>3PM</th>
            <th>PTS</th>
            <th>REB</th>
            <th>AST</th>
            <th>STL</th>
            <th>BLK</th>
            <th>TO</th>
          </tr>
        </thead>


          <tbody>
            {data.map((p, i) => (
            <tr key={i}>
              <td>{i + 1}</td> {/* Rank */}
              <td>{p.name}</td>
              <td>{p.features[0]}</td>
              <td>{p.features[1]}</td>
              <td>{p.fg_pct}</td>
              <td>{p.ft_pct}</td>
              <td>{p.three_pm}</td>
              <td>{p.pts}</td>
              <td>{p.reb}</td>
              <td>{p.ast}</td>
              <td>{p.stl}</td>
              <td>{p.blk}</td>
              <td>{p.to}</td>
            </tr>
            
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default App;
