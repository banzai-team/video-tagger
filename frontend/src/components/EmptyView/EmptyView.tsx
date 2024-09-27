import React from "react";

type EmptyViewProps = {
  title: string | React.ReactNode;
  description?: string | React.ReactNode;
  children?: string | React.ReactNode;
};

const EmptyView: React.FC<EmptyViewProps> = ({title, description, children}) => {
  return (
    <div
        className="text-gray-500 w-full h-2/3 flex flex-col justify-center items-center gap-2 md:gap-4"
    >
      <h2 className="text-accent">{title}</h2>
      <div className="text-gray-500">{description}</div>
      <div>{children}</div>
    </div>
  );
};
export default EmptyView;
