// generated with @7nohe/openapi-react-query-codegen@1.6.1 

import { UseQueryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { SystemProbsService, VideoManagementService } from "../requests/services.gen";
import * as Common from "./common";
export const useVideoManagementServiceListVideosV1ListVideosGetSuspense = <TData = Common.VideoManagementServiceListVideosV1ListVideosGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>(queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useSuspenseQuery<TData, TError>({ queryKey: Common.UseVideoManagementServiceListVideosV1ListVideosGetKeyFn(queryKey), queryFn: () => VideoManagementService.listVideosV1ListVideosGet() as TData, ...options });
export const useSystemProbsServiceHealthHealthGetSuspense = <TData = Common.SystemProbsServiceHealthHealthGetDefaultResponse, TError = unknown, TQueryKey extends Array<unknown> = unknown[]>(queryKey?: TQueryKey, options?: Omit<UseQueryOptions<TData, TError>, "queryKey" | "queryFn">) => useSuspenseQuery<TData, TError>({ queryKey: Common.UseSystemProbsServiceHealthHealthGetKeyFn(queryKey), queryFn: () => SystemProbsService.healthHealthGet() as TData, ...options });
