import React from 'react';
import { useFormik } from 'formik';
// import { CardContent, CardFooter } from '~/components/ui/card';
// import { Input } from '~/components/ui/input';
// import { Button } from '~/components/ui/button';
// import Dropzone from "~/components/Dropzone";
import {FileCheck2, X} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import {Spinner} from "@/components/ui/spinner.tsx";
import Dropzone from "@/components/Dropzone";
import {Input} from "@/components/ui/input.tsx";
// import {Spinner} from "~/components/ui/spinner";

type AddVacancyFormProps = {
  onSubmit: (values: { link?: string; files?: any, title?: string; description?: string; }) => Promise<any>;
};

const AddVideoForm: React.FC<AddVacancyFormProps> = ({ onSubmit }) => {
  const formik = useFormik<{
    link: string;
    title: string;
    description: string;
    files: {
      path: string;
      type: "file" | "folder";
      name: string;
      mimeType: string;
      data: string;
      size: number;
    }[] | null
  }>({
    initialValues: {
      title: "",
      description: "",
      link: "",
      files: null,
    },
    onSubmit: async (values, {setSubmitting}) => {
      setSubmitting(true);
      await onSubmit(values);
      setSubmitting(false);
    },
    // validationSchema,
  });


  return (
    <form onSubmit={formik.handleSubmit}>
      <div className="grid gap-4 md:grid-cols-1
        lg:grid-cols-2"
      >
        <div>
          <div className="text-xs text-gray-800 pb-1">ID или ссылка на видео</div>
          <Input placeholder="Введите данные видео" {...formik.getFieldProps('link')} disabled={!!formik.values.files} />
        </div>

        <div className="flex flex-col lg:flex-row">
          <div className="py-5 gap-4 text-md text-muted-foreground/50 flex flex-row items-center lg:py-0 lg:pr-10 lg:flex-col md:gap-2">
            <div className="w-full h-px bg-muted-foreground/20 lg:w-px lg:h-full" />
            или
            <div className="w-full h-px bg-muted-foreground/20 lg:w-px lg:h-full" />
          </div>
          <div className="flex flex-col gap-3">
            <div>
              <div className="text-xs text-gray-800 pb-1">Заголовок видео</div>
              <Input placeholder="Введите данные видео" {...formik.getFieldProps('title')}
                     disabled={!!formik.values.link}/>
            </div>
            <div>
              <div className="text-xs text-gray-800 pb-1">Описание видео</div>
              <Input placeholder="Введите данные видео" {...formik.getFieldProps('description')}
                     disabled={!!formik.values.link}/>
            </div>
            <div>
              <div className="text-xs text-gray-800 pb-1">Видеофайл</div>
              {
                formik.values.files
                    ? (
                        <div className="flex flex-row gap-4">
                          <div
                              style={{backgroundImage: 'url(/round.svg)'}}
                              className="bg-center bg-no-repeat bg-cover relative p-4 flex h-36 w-40 flex-col items-center justify-center rounded-md bg-zinc-100 md:p-10 md:h-48"
                          >
                            <Button className="absolute top-1 right-0" variant="ghost" size="sm"
                                    onClick={() => formik.setFieldValue("files", null)}>
                              <X className="text-destructive h-6 w-6 cursor-pointer hover:opacity-50"/>
                            </Button>
                            <FileCheck2 className="h-8 w-8 text-primary"/>
                          </div>
                          <div>
                            <div
                                className="font-medium pt-2 whitespace-nowrap overflow-hidden overflow-ellipsis max-w-24 md:max-w-32 lg:max-w-52 xl:max-w-80">{formik.values.files[0].name}</div>
                            <div
                                className="text-xs text-gray-800 pt-1">{(formik.values.files[0].size / 1024 / 1024).toFixed(2)}Мб
                            </div>
                          </div>
                        </div>
                    )
                    : (
                        <Dropzone onDrop={(acceptedFiles: any[]) => {
                          acceptedFiles.forEach((file) => {
                            const reader = new FileReader()

                            reader.onabort = () => console.log('file reading was aborted')
                            reader.onerror = () => console.log('file reading has failed')
                            reader.onload = () => {
                              // Do whatever you want with the file contents
                              // const binaryStr = reader.result
                              formik.setFieldValue("files", [file]);
                            }
                            reader.readAsArrayBuffer(file)
                          })
                        }}
                                  disabled={!!formik.values.link}
                                  acceptTypes={{
                                    "video/mp4": [".mp4"],
                                    "video/mpeg": [".mpeg"],
                                    "video/mov": [".mov"],
                                    "video/webm": [".webm"]
                                  }}
                        />
                    )
              }
            </div>
          </div>
        </div>
      </div>

      <div className="justify-end">
        {
          formik.isSubmitting
              ? <Spinner className="my-1"/>
              : (
                  <Button type="submit" disabled={!formik.values.link && !formik.values.files}>
                    Добавить
                  </Button>
              )
        }
      </div>
    </form>
  );
};

export default AddVideoForm;
