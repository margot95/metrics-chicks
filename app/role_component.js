import React from 'react';
import './role_component.module.css';  // Import your CSS file

const RoleComponent = ({ m }) => {
  // Determine the class based on the value of m.role
  const roleClass = m.role === 'user' ? 'user-style' : 'ai-style';

  return (
    <div className={roleClass}>
      {m.role === 'user' ? 'User: ' : 'AI: '}
      {/* Other content goes here */}
    </div>
  );
};

export default RoleComponent;
