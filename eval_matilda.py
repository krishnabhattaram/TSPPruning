# wrapper = model_utils.modelWrapper(
#     model=model,
#     function_names=function_names,
#     threshold=threshold
# )

# printer = pprint.PrettyPrinter(indent=4)

# X_test, y_test = train_loader.load_testing_features(), train_loader.load_testing_labels()
# X_test, y_test = np.vstack(X_test), np.concatenate(y_test)

# if threshold is not None:
#     y_test_pred = (wrapper.predict_proba_vector(X_test) > threshold).astype(int)
# else:
#     y_test_pred = wrapper.predict_vector(X_test)

# metrics = {
#     "accuracy": train_utils.accuracy(y_test, y_test_pred),
#     "false_negative_rate": train_utils.false_negative_rate(y_test, y_test_pred),
#     "pruning_rate": train_utils.pruning_rate(y_test_pred),
# }

# print("Results: ")
# printer.pprint(metrics)
