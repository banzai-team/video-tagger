// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseQueryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { InferenceEndpointsService, SystemProbsService } from "../requests/services.gen";
import * as Common from "./common";
export const useInferenceEndpointsServiceGetVideoByIdV1VideosIdGetSuspense = <TData = Common.InferenceEndpointsServiceGetVideoByIdV1VideosIdGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>({ id }: {
  id: unknown;
}, queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useSuspenseQuery<TData, TError>({ queryKey: Common.UseInferenceEndpointsServiceGetVideoByIdV1VideosIdGetKeyFn({ id }, queryKey), queryFn: () => InferenceEndpointsService.getVideoByIdV1VideosIdGet({ id }) as TData, ...options });
export const useInferenceEndpointsServiceGetVideosV1VideosGetSuspense = <TData = Common.InferenceEndpointsServiceGetVideosV1VideosGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>({ size, skip }: {
  size?: unknown;
  skip?: unknown;
} = {}, queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useSuspenseQuery<TData, TError>({ queryKey: Common.UseInferenceEndpointsServiceGetVideosV1VideosGetKeyFn({ size, skip }, queryKey), queryFn: () => InferenceEndpointsService.getVideosV1VideosGet({ size, skip }) as TData, ...options });
export const useSystemProbsServiceHealthHealthGetSuspense = <TData = Common.SystemProbsServiceHealthHealthGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>(queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useSuspenseQuery<TData, TError>({ queryKey: Common.UseSystemProbsServiceHealthHealthGetKeyFn(queryKey), queryFn: () => SystemProbsService.healthHealthGet() as TData, ...options });
