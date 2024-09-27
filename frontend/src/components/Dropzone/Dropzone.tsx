import { FileVideo2 } from "lucide-react";
import React from "react";
import { useDropzone } from "react-dropzone";

type DropzoneProps = {
  disabled?: boolean;
  onDrop: any;
  acceptTypes?: any
};

const Dropzone: React.FC<DropzoneProps> = ({onDrop, acceptTypes, disabled}) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: acceptTypes,
    onDrop: (acceptedFiles) => onDrop(acceptedFiles),
  });

  return (
    <div
      {...getRootProps({ className: "dropzone" })}
      className="bg-center bg-no-repeat bg-cover dropzone cursor-pointer p-1 flex h-32 w-full flex-col items-center justify-center rounded-md border border-dashed border-gray-300 md:h-32 lg:w-96 md:p-5"
      style={disabled ? {opacity: 0.5, cursor: "auto"} : {}}
    >
      <input {...getInputProps()} disabled={disabled} />
      <FileVideo2 className="h-8 w-8 md:h-9 md:w-9 text-accent" />
      <div className="text-center">
        {isDragActive ? (
          <p className="text-xs text-muted-foreground pt-3">Перетаскивать сюда сюда ...</p>
        ) : (
          <p className="text-xs text-muted-foreground pt-3">Загрузите видео, нажав сюда или перетащив его</p>
        )}
      </div>
    </div>
  );
};
export default Dropzone;
