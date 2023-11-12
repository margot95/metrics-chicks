"use client";

import { useMemo } from "react";
import { useChat } from "ai/react";
import RoleComponent from "./role_component"

type DataType = {
  context: any[];
};

export default function Chat() {
  const { messages, data, input, handleInputChange, handleSubmit } = useChat();

  const parsedData = useMemo<DataType[]>(
    () => data?.flatMap((x: string) => [null, JSON.parse(x)]),
    [data]
  );

  return (
    <div className="mx-auto w-full max-w-md py-24 flex flex-col stretch overflow-scroll">
      {messages.length > 0
        ? messages.map((m, i) => (
          <div key={m.id} className="flex flex-col mb-6">
            <b>{m.role === "user" ? "You: " : "Simp!Law: "}</b>

              <RoleComponent m={m} parsedData={parsedData} i={i} />
          ))
        : null}

      <form onSubmit={handleSubmit}>
        <input
          className="fixed w-full max-w-md bottom-0 border border-gray-300 rounded mb-8 shadow-xl p-2"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>



  );
}
