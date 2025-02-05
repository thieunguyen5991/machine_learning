import math

from pandas import DataFrame

from __init__fuzzy import *


def experiment(sliding_number=3, hidden_node=15):
    # result = []
    print "New loop"
    X_train_size = int(len(u_class_transform) * 0.7)
    sliding = np.array(list(SlidingWindow(u_class_transform, sliding_number)))
    sliding = np.array(sliding, dtype=np.int32)
    X_train = sliding[:X_train_size]
    y_train = u_class_transform[sliding_number:X_train_size + sliding_number]
    X_test = sliding[X_train_size:]
    y_test = u_class_transform[X_train_size + sliding_number - 1:]
    y_actual_test = dat[X_train_size + sliding_number - 1:].tolist()
    # # Define classifier
    n_hidden = len(X_train[0]) + sliding_number

    fit_params = {
        'neural_shape': [len(X_train[0]), n_hidden, 1]
    }
    ga_estimator = GAEstimator(cross_rate=0.5, mutation_rate=0.02, gen_size=100, pop_size=50)
    nn = NeuralFlowRegressor(hidden_nodes=[n_hidden],steps=4000, learning_rate=1E-03,cv=True)
    classifier = OptimizerNNEstimator(ga_estimator, nn)

    a = classifier.fit(X_train, y_train, **fit_params)
    ypred = np.round(abs(classifier.predict(X_test))).flatten()
    ypred_defuzzy = [defuzzy(item, u_unique_mapping, u_midpoints) for item in ypred]
    score_mape = mean_absolute_error(ypred_defuzzy, y_actual_test)
    score_rmse = math.sqrt(mean_squared_error(ypred_defuzzy, y_actual_test))
    np.savez('model_saved/fuzzy_GABPNN_%s_%s' % (sliding_number, score_mape), y_pred=ypred_defuzzy, y_true=y_actual_test)
    return sliding_number, score_rmse, score_mape

result = [[experiment(sliding_number=i) for i in np.arange(2,6)] for j in np.arange(10)]
#np.savez("BPNN_epochs",result=result)
results = DataFrame(np.array(result).reshape(-1,3), columns=["sliding_number","rmse","mae"])
results.to_csv('experiment_logs/fgabpnn_experiment.csv')
