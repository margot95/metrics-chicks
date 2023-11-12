import React from 'react';
import { userClasses, aiClasses } from './RoleClasses';

const RoleComponent = ({ m, parsedData, i }) => {
  const roleClasses = m.role === 'user' ? userClasses : aiClasses;

  console.log('parsedData:', parsedData);
  console.log('context:', parsedData?.[i]?.context);


  return (
    <>
    <div className="chat-body">
    <div key={m.id} className={roleClasses.mainClass}>
      <div className='box'>
        <div className={roleClasses.titleClass}>

      {m.role === 'user' ? 'User: ' : 'simp!LAW: '}
      <div className={roleClasses.linkClass}>
      <small className="source">
              {parsedData?.[i]?.context?.map(({ payload }, index, array) => (
                <React.Fragment key={index}>
                  <a href={payload.link} target="_blank" rel="noopener noreferrer">
                    {payload.article}
                  </a>
                  {index < array.length - 1 && ' | '}
                </React.Fragment>
              ))}
      </small>
      </div>
      </div>
    <p className="whitespace-pre-wrap">{m.content.trim()}</p>
    </div>
    </div>
    </div>
    </>

  );
};

export default RoleComponent;
