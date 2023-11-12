import React from 'react';
import { userClasses, aiClasses } from './RoleClasses';

const RoleComponent = ({ m, parsedData, i }) => {
  const roleClasses = m.role === 'user' ? userClasses : aiClasses;

  return (
    <>
    <div className={roleClasses.borderClass}>
    <div key={m.id} className={`flex flex-col mb-6 ${roleClasses.mainClass}`}>

      {m.role === 'user' ? 'User: ' : 'AI: '}
      <small className="source">
              {parsedData?.[i]?.context?.map(({ payload }, index, array) => (
                <span key={index}>
                  <a href={payload.link} target="_blank" rel="noopener noreferrer">
                    {payload.article}
                  </a>
                  {index < array.length - 1 && ' | '}
                </span>
              ))}
      </small>
    </div>
    <p className="whitespace-pre-wrap">{m.content.trim()}</p>
    </div>
    </>

  );
};

export default RoleComponent;
