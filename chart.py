import matplotlib.pyplot as plt


def chart(reviews, title):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])

    x_dimension = list()
    y_dimension = list()

    for review in reviews:
        x_dimension.append(review)
        y_dimension.append(reviews[review])

    ax.set_title(title)
    ax.bar(x_dimension, y_dimension)
    plt.show()
