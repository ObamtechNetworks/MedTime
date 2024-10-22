import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const GoalOverview = ({ progressPercentage, totalDays, daysRemaining }) => {
  return (
    <div className="goal-overview">
      <h3>Goal Overview</h3>
      <div style={{ width: '150px', height: '150px' }}>
        <CircularProgressbar
          value={progressPercentage}
          text={`${progressPercentage}%`}
          styles={buildStyles({
            pathColor: `rgba(62, 152, 199, ${progressPercentage / 100})`,
            textColor: '#f88',
            trailColor: '#d6d6d6',
          })}
        />
      </div>
      <p>Total Days: {totalDays}</p>
      <p>Days Remaining: {daysRemaining}</p>
    </div>
  );
};

export default GoalOverview;
