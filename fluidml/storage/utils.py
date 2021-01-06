from collections import defaultdict
from typing import Dict, Any, List

from fluidml.common import Task
from fluidml.common.exception import TaskResultKeyAlreadyExists
from fluidml.storage import ResultsStore


def pack_results(all_tasks: List[Task],
                 results_store: ResultsStore,
                 return_results: bool = True) -> Dict[str, Any]:
    results = defaultdict(list)
    if return_results:
        for task in all_tasks:
            result = results_store.get_results(task_name=task.name,
                                               task_unique_config=task.unique_config,
                                               task_publishes=task.publishes)
            results[task.name].append({'result': result,
                                       'config': task.unique_config})
    else:
        for task in all_tasks:
            results[task.name].append(task.unique_config)

    return simplify_results(results=results)


def pack_predecessor_results(predecessor_tasks: List[Task],
                             results_store: ResultsStore,
                             reduce_task: bool) -> Dict[str, Any]:
    if reduce_task:
        all_results = []
        for predecessor in predecessor_tasks:
            result = results_store.get_results(task_name=predecessor.name,
                                               task_unique_config=predecessor.unique_config,
                                               task_publishes=predecessor.publishes)
            all_results.append({'result': result,
                                'config': predecessor.unique_config})
        return {"reduced_results": all_results}

    else:
        results = {}
        for predecessor in predecessor_tasks:
            result = results_store.get_results(task_name=predecessor.name,
                                               task_unique_config=predecessor.unique_config,
                                               task_publishes=predecessor.publishes)
            for key, value in result.items():
                if key in results.keys():
                    raise TaskResultKeyAlreadyExists(
                        f"{predecessor.name} saves a key '{key}' that already exists in another tasks's result")
                else:
                    results[key] = value
    return results


def simplify_results(results: Dict[str, Any]) -> Dict[str, Any]:
    for task_name, task_results in results.items():
        if len(task_results) == 1:
            results[task_name] = task_results[0]
    return results
