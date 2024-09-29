import { useFormik } from 'formik';
// import { CardContent, CardFooter } from '~/components/ui/card';
// import { Input } from '~/components/ui/input';
// import { Button } from '~/components/ui/button';
// import Dropzone from "~/components/Dropzone";
import { FileVideo2, X } from "lucide-react";
import { Button } from "@/components/ui/button.tsx";
import { Spinner } from "@/components/ui/spinner.tsx";
import Dropzone from "@/components/Dropzone";
import { Input } from "@/components/ui/input.tsx";
// import {Spinner} from "~/components/ui/spinner";
import * as Yup from "yup";

type AddVacancyFormProps = {
  onSubmit?: (values: { link?: string; files?: any, title?: string; description?: string; }) => Promise<any>;
};

const validationSchema = Yup.object({
  files: Yup.mixed().nullable(),
  title: Yup.string().when('files', {
    is: value => value !== null,
    then: schema => schema.required('Required field')
  }),
  description: Yup.string().when('files', {
    is: value => value !== null,
    then: schema => schema.required('Required field')
  })
})

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
    onSubmit: async (values, { setSubmitting }) => {
      setSubmitting(true);
      await onSubmit(values);
      setSubmitting(false);
    },
    validationSchema,
  });

  const titleError = formik.touched?.title && formik.errors?.title ? formik.errors.title : "";
  const titleColor = titleError ? 'text-red-500' : 'text-gray-800'

  const descriptionError = formik.touched?.description && formik.errors?.description ? formik.errors.description : "";
  const descriptionColor = descriptionError ? 'text-red-500' : 'text-gray-800'

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
              <div className={`text-xs pb-1 ${titleColor}`}>Заголовок видео{formik.values.files && "*"}</div>
              <Input placeholder="Введите данные видео" {...formik.getFieldProps('title')}
                disabled={!!formik.values.link} />
            </div>
            <div>
              <div className={`text-xs pb-1 ${descriptionColor}`}>Описание видео{formik.values.files && "*"}</div>
              <Input placeholder="Введите данные видео" {...formik.getFieldProps('description')}
                disabled={!!formik.values.link} />
            </div>
            <div>
              <div className="text-xs text-gray-800 pb-1">Видеофайл</div>
              {
                formik.values.files
                  ? (
                    <div className="flex flex-row gap-4">
                      <div
                        style={{ backgroundImage: 'url(/round.svg)' }}
                        className="bg-center bg-no-repeat bg-cover relative p-4 flex h-14 w-32 flex-col items-center justify-center rounded-md bg-zinc-100 md:p-2 md:h-20"
                      >
                        <Button className="absolute top-1 right-1" variant="ghost" size="xs"
                          onClick={() => formik.setFieldValue("files", null)}>
                          <X className=" h-5 w-5 cursor-pointer hover:opacity-50" />
                        </Button>
                        <FileVideo2 className="h-8 w-8 text-accent" />
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

      <div className="justify-end pt-4 lg:pt-0">
        {
          formik.isSubmitting
            ? <Spinner className="my-1" />
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
