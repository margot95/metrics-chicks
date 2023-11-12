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
    <div className="">
      {messages.length > 0
        ? messages.map((m, i) => (

              <RoleComponent m={m} parsedData={parsedData} i={i} />
          ))
        : null}

      <form onSubmit={handleSubmit}>
        <input
          className=" chat-input"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>



  );
}
